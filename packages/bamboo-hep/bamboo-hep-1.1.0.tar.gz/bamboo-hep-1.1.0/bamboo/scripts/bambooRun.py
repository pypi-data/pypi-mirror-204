"""
Command-line script: run an analysis module

Loads a class from a module (import path or file),
constructs an instance with the remaining arguments to parse,
and runs it
"""

import argparse
import importlib.util
import logging
import os.path


def main():
    parser = argparse.ArgumentParser(description="Run an analysis module", add_help=False)
    parser.add_argument("-m", "--module", type=str,
                        default="bamboo.analysismodules:AnalysisModule",
                        help="Module to run (format: modulenameOrPath[:classname])")
    parser.add_argument("--help", "-h", action="store_true",
                        help="Print this help message and exit")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Run in verbose mode")
    args, remArgs = parser.parse_known_args()
    # pass arguments on
    remArgs.append(f"--module={args.module}")
    if args.help:
        remArgs.append("--help")
    if args.verbose:
        remArgs.append("--verbose")

    logModules = [f"bamboo.{bMod}" for bMod in (
        "analysismodules", "analysisutils",
        "batch", "batch_slurm", "batch_htcondor",
        "dataframebackend", "treeoperations", "treedecorators", "plots")]
    logLevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=logLevel)  # FIXME specify a handler
    for logMod in logModules:
        modLogger = logging.getLogger(logMod)
        modLogger.setLevel(logLevel)

    modArg = args.module
    clName = None
    if ":" in modArg:
        if modArg.count(":") > 1:
            raise RuntimeError(f"More than one : in module argument '{modArg}'")
        modArg, clName = tuple(modArg.split(":"))
    # modArg should now be a python module name or path now
    spec = None
    try:
        spec = importlib.util.find_spec(modArg)
    except Exception:
        pass
    if spec:  # is a module
        if not clName:
            clName = spec.split(".")[-1]
    elif os.path.exists(modArg):
        modName = os.path.splitext(os.path.basename(modArg))[0]
        if not clName:
            clName = modName
        spec = importlib.util.spec_from_file_location(modName, modArg)
    else:
        raise RuntimeError(
            f"Module argument '{modArg}' is neither "
            "an importable module or an existing path")
    # do the import
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, clName):
        raise RuntimeError(
            "Module {0} has no class with name {1}, "
            "please specify it using --module=modulenameOrPath:classname")
    modCls = getattr(mod, clName)
    modInst = modCls(remArgs)
    modInst.run()
