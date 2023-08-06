"""
Batch cluster tools (common part for HTCondor and slurm, potentially others)
"""

import logging
import os
import os.path
import signal
import subprocess
import time
from collections import defaultdict
from datetime import datetime
from itertools import chain
from threading import Event

from . import utils

logger = logging.getLogger(__name__)


def format_runtime(td):
    sec = td.total_seconds()
    mins = sec // 60
    sec -= mins * 60
    hrs = mins // 60
    mins -= hrs * 60
    return f"{hrs:02.0f}:{mins:02.0f}:{sec:02.3f}"


class CommandListJob:
    """
    Interface/base for 'backend' classes to create a job cluster/array from a list of commands

    each command becomes an subjob in the array/cluster
    """
    def __init__(self, commandList, workDir=None, workdir_default_pattern="batch_work"):
        self.commandList = commandList
        self.workDir = self.init_dirtowrite(workDir, default_pattern=workdir_default_pattern)
        self.workDirs = self.setupBatchDirs(self.workDir)

    # interface methods
    def submit(self):
        """ Submit the job(s) """
        pass

    def cancel(self):
        """ Cancel the job(s) """
        pass

    def commandOutFiles(self, command):
        """ Output files for a given command (when finished) """
        pass
    # for monitoring
    @property
    def status(self):
        """ overall job status summary """
        pass

    def statuses(self):
        """ list of subjob statuses (numeric, using indices in CondorJobStatus) """
        pass

    def updateStatuses(self):
        """ Update the subjob status cache (if used in the implementation) """
        pass

    def subjobStatus(self, i):
        """ get status of subjob """
        pass

    def commandStatus(self, command):
        """ get the status of the jobs corresponding to one of the commands """
        pass

    def getID(self, command):
        """ job identifier for command """
        pass

    def getLogFile(self, command):
        """ get path to log file corresponding to the given command """
        pass

    def getResubmitCommand(self, failedCommands):
        """
        return a suggestion command the user should run to resubmit
        a job array with only the failed commands
        """
        pass

    def getRuntime(self, commands):
        """ get the runtime of a command (should be valid when finished) """
        pass

    # helper methods
    @staticmethod
    def init_dirtowrite(given=None, default_pattern="batch"):
        """ Initialisation helper: check that the directory does not exist, then create it

        If None is given, a default ("$(pwd)/{default_pattern}", "$(pwd)/default_pattern_0" etc.) is used
        """
        if given is None:
            test_dir = os.path.join(utils.getlcwd(), default_pattern)
            if os.path.exists(test_dir):
                i = 0
                while os.path.exists(test_dir) and i < 10:
                    test_dir = os.path.join(utils.getlcwd(), f"{default_pattern}_{i:d}")
                    i += 1
        else:
            test_dir = given
        if os.path.exists(test_dir):
            raise RuntimeError(f"Directory {test_dir} exists")

        os.makedirs(test_dir)

        return utils.labspath(test_dir)  # make sure we keep absolute paths

    @staticmethod
    def setupBatchDirs(workDir):
        """ Create up the working directories (input, output, logs) under workDir """
        dirs = {
            "in": os.path.join(workDir, "input"),
            "out": os.path.join(workDir, "output"),
            "log": os.path.join(workDir, "logs")
        }
        for subdir in dirs.values():
            os.mkdir(subdir)
        logger.info(f"Created working directories under {workDir}")
        return dirs


class SplitAggregationTask:
    """ Task split in commands, whose results can be merged """
    def __init__(self, commandList, finalizeAction=None):
        self._jobCluster = None
        self.commandList = commandList
        self.finalizeAction = finalizeAction
        self.failedCommands = []

    @property
    def jobCluster(self):
        return self._jobCluster

    @jobCluster.setter
    def jobCluster(self, jobCluster):
        if self._jobCluster:
            raise Exception("SplitAggregationTask.jobCluster has already been set")
        self._jobCluster = jobCluster
        if self.finalizeAction:  # pass it on
            self.finalizeAction.jobCluster = jobCluster

    def tryFinalize(self, completedStatus, failedStatuses=None):
        """Return True if all jobs have finished running (either failed or completed)"""
        if not self.jobCluster:
            return False

        nFailed, nSuccess = 0, 0
        for cmd in self.commandList:
            cmdStatus = self.jobCluster.commandStatus(cmd).upper()
            if failedStatuses and cmdStatus in failedStatuses:
                nFailed += 1
                if cmd not in self.failedCommands:
                    logger.error(f"Batch job failed for the command {cmd}")
                    logger.error(f"The corresponding log file is in {self.jobCluster.getLogFile(cmd)}")
                    self.failedCommands.append(cmd)
                    if nFailed == 1:
                        logger.error(
                            "After identifying and solving the reason of failure, "
                            "this job can be resubmitted with the following command:"
                        )
                        logger.error(f"  {' '.join(self.jobCluster.getResubmitCommand([cmd]))}")
                        logger.error(
                            "This message is only printed for the first failing job, "
                            "but the IDs of all (initially) failing jobs will be printed "
                            "by the monitoring loop, " "so the most convenient is probably "
                            "to wait until all jobs affected by the same problem to fail, "
                            "and then resubmit them together "
                            "(the resubmission commands accept comma-separated lists of job IDs)."
                        )
            elif cmdStatus == completedStatus:
                nSuccess += 1

        if nSuccess + nFailed == len(self.commandList):
            if nSuccess == len(self.commandList):
                if self.finalizeAction:
                    self.finalizeAction.perform()
            else:
                logger.error(
                    f"Task failed, {len(self.failedCommands)} out of {len(self.commandList)} "
                    "commands returned a non-zero exit code or could not be run.")
                if self.finalizeAction:
                    logger.error("Skipping finalization step since there were failed commands.")
            return True

        return False


class Action:
    """ interface for job finalization """
    def getActions(self):
        """ interface method """
        return []

    def perform(self):
        """ interface method """
        return False


class HaddAction(Action):
    """ merge results with hadd
    """
    def __init__(self, commandList, outDir, options=None):
        self.jobCluster = None
        self.commandList = commandList
        self.outDir = outDir
        self.options = options if options is not None else []
        super().__init__()

    def getActions(self):
        """ Get list of commands to be run """

        if len(self.commandList) == 0:    # nothing
            return []
        elif len(self.commandList) == 1:  # move
            cmd = self.commandList[0]
            return [["mv", outf, self.outDir] for outf in self.jobCluster.commandOutFiles(cmd)]
        else:                             # merge
            actions = []
            # collect for each output file name which jobs produced one
            filesToMerge = dict()
            for cmd in self.commandList:
                for outf in self.jobCluster.commandOutFiles(cmd):
                    outfb = os.path.basename(outf)
                    if outfb not in filesToMerge:
                        filesToMerge[outfb] = []
                    filesToMerge[outfb].append(outf)

            for outfb, outfin in filesToMerge.items():
                fullout = os.path.join(self.outDir, outfb)
                actions.append(["hadd"] + self.options + [fullout] + outfin)
            return actions

    def perform(self):
        """ Perform actual hadd/move."""

        for action in self.getActions():
            logger.info("Finalization: calling {}".format(" ".join(action)))
            try:
                stdout = subprocess.DEVNULL if "hadd" in action else None
                subprocess.check_call(action, stdout=stdout)
            except subprocess.CalledProcessError:
                logger.error("Failed to run the finalization command:")
                logger.error(" ".join(action))


class TasksMonitor:
    """ Monitor a number of tasks and the associated job clusters """
    def __init__(self, jobs, tasks, interval=120,
                 allStatuses=None, activeStatuses=None, failedStatuses=None, completedStatus=None):
        """ Constructor

        jobs: job clusters to monitor
        tasks: tasks to monitor (and finalize)
        interval: number of seconds between status checks
        """
        self.jobs = set()
        self.tasks = set()
        self.activeTasks = set()
        self.add(jobs, tasks)
        self.interval = interval
        self.allStatuses = list(allStatuses) if allStatuses else []
        self.activeStatuses = list(activeStatuses) if activeStatuses else []
        self.failedStatuses = list(failedStatuses) if failedStatuses else []
        self.completedStatus = completedStatus

    def add(self, jobs, tasks):
        """ add jobs and tasks """
        self.jobs.update(jobs)
        self.tasks.update(tasks)
        # assumption: same set of commands
        assert (sum(len(j.commandList) for j in self.jobs)
                == sum(len(t.commandList) for t in self.tasks))
        self.activeTasks.update(tasks)

    @staticmethod
    def makeStats(statuses, allStatuses):
        histo = [0 for st in allStatuses]
        for jSt in statuses:
            histo[jSt] += 1
        return histo

    @staticmethod
    def formatStats(stats, allStatuses):
        return "{} / {:d} Total".format(
            ", ".join(f"{n:d} {nm}" for n, nm in zip(stats, allStatuses) if n > 0),
            sum(stats))

    def _shouldTryFinalize(self, prevStats, stats):
        """ determine if finalization should be tried: has any job finished (either successfully or not?) """
        if stats[self.completedStatus] > prevStats[self.completedStatus]:
            return True
        for st in self.failedStatuses:
            if stats[st] > prevStats[st]:
                return True
        return False

    def _tryFinalize(self):
        """ try to finalize tasks """
        finalized = []
        for t in self.activeTasks:
            if t.tryFinalize(
                    self.allStatuses[self.completedStatus],
                    [self.allStatuses[i] for i in self.failedStatuses]):
                finalized.append(t)  # don't change while iterating
        for ft in finalized:
            self.activeTasks.remove(ft)
        if len(finalized) > 0:
            logger.info(f"Finalized {len(finalized):d} tasks, {len(self.activeTasks):d} remaining")

    def collect(self, wait=None):
        """ Wait for the jobs to finish, then finalize tasks.

        Returns True if every job succeeded, otherwise return False.
        """

        collectResult = {"success": True}

        exitEvent = Event()

        def exitLoop(signal, _frame):
            resp = input("Do you really want to cancel all jobs and exit (y/n)? ")
            if resp.lower() == "y":
                for j in self.jobs:
                    j.cancel()
                exitEvent.set()
        signal.signal(signal.SIGINT, exitLoop)

        for j in self.jobs:
            j.updateStatuses()
        self._tryFinalize()
        if len(self.activeTasks) > 0:
            logger.info("Waiting for jobs to finish...")
            if wait:
                time.sleep(wait)
            stats = self.makeStats(chain.from_iterable(j.statuses() for j in self.jobs), self.allStatuses)
            while (len(self.activeTasks) > 0
                   and sum(stats[sa] for sa in self.activeStatuses) > 0
                   and not exitEvent.is_set()):
                exitEvent.wait(self.interval)
                prevStats = stats
                stats = self.makeStats(chain.from_iterable(j.statuses() for j in self.jobs), self.allStatuses)
                if self._shouldTryFinalize(prevStats, stats):
                    self._tryFinalize()
                failedMsg = ""
                if any(task.failedCommands for task in self.tasks):
                    failedMsg = " ; failed: {}".format(",".join(
                        str(task.jobCluster.getID(cmd))
                        for task in self.tasks
                        for cmd in task.failedCommands))
                logger.info("[ {} :: {}{} ]".format(
                    datetime.now().strftime("%H:%M:%S"),
                    self.formatStats(stats, self.allStatuses),
                    failedMsg))
        # Check for failed tasks, retrieve all failed commands:
        if any(task.failedCommands for task in self.tasks):
            logFiles = "\n".join(
                task.jobCluster.getLogFile(cmd) for task in self.tasks
                for cmd in task.failedCommands if cmd in task.commandList
            )
            logger.error(f"Some tasks failed to run. The log files of the failed batch jobs are:\n{logFiles}")
            failedCommands = [cmd for task in self.tasks for cmd in task.failedCommands]
            logger.error("The full list of commands that failed or was not run is:\n{}".format(
                "\n".join(failedCommands)))
            collectResult["success"] = False
            failedCommandsPerCluster = defaultdict(list)
            for task in self.tasks:
                failedCommandsPerCluster[task.jobCluster] += task.failedCommands
            resubmitCommands = [cluster.getResubmitCommand(commands)
                                for cluster, commands in failedCommandsPerCluster.items()]
            if any(resubmitCommands):
                logger.error("Resubmitting the failed jobs can be done by running:\n{}".format(
                    "\n".join(" ".join(cmd) for cmd in resubmitCommands)))
                collectResult["resubmitCommands"] = resubmitCommands

        return collectResult


def splitInChunks(theList, nChunks=None, chunkLength=None):
    if (nChunks is None) == (chunkLength is None):
        raise ValueError(
            f"One and only one of nChunks or chunkLength should be specified, "
            "got {nChunks} and {chunkLength}")
    N = len(theList)
    if nChunks is not None:
        import math
        chunkLength = int(math.ceil(1. * N / nChunks))
    for iStart, iStop in zip(
            range(0, len(theList), chunkLength),
            range(chunkLength, len(theList) + chunkLength, chunkLength)):
        yield theList[iStart:min(iStop, N)]


def writeFileList(fileList, outName):
    if os.path.isfile(outName):
        with open(outName) as ffile:
            ffiles = [ln.strip() for ln in ffile if len(ln.strip()) > 0]
        if sorted(ffiles) == sorted(fileList):
            return
        else:
            logger.warning(f"Overwriting {outName} with a new list of {len(fileList):d} files")
    with open(outName, "w") as nfile:
        nfile.write("\n".join(fileList))


def getBackend(name):
    if name == "slurm":
        from . import batch_slurm as batchBackend
    elif name == "htcondor":
        from . import batch_htcondor as batchBackend
    else:
        raise RuntimeError(f"Unknown backend: {name}")
    return batchBackend
