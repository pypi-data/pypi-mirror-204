"""
The :py:mod:`bamboo.scalefactors` module contains helper methods
for configuring scale factors, fake rates etc.

The basic configuration parameter is the JSON file path for a set of scalefactors.
There two basic types are

- lepton scale factors (dependent on a number of object variables, e.g. pt and eta),
- jet (b-tagging) scale factors (grouped set for different flavours, for convenience)

Different values (depending on the data-taking period)
can be taken into account by weighting or by randomly sampling.
"""
__all__ = ("get_scalefactor", "lumiPerPeriod_default", "binningVariables_nano", "BtagSF", "get_correction",
           "get_bTagSF_fixWP", "makeBtagWeightMeth1a", "get_bTagSF_itFit", "makeBtagWeightItFit")

import logging
from functools import partial
from itertools import chain

from . import treefunctions as op

logger = logging.getLogger(__name__)


#: Integrated luminosity (in 1/pb) per data taking period
lumiPerPeriod_default = {
    # 2016 - using approved normtag + 07Aug2017 re-reco golden JSON
    # ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt
    "Run2016B": 5750.491,
    "Run2016C": 2572.903,
    "Run2016D": 4242.292,
    "Run2016E": 4025.228,
    "Run2016F": 3104.509,
    "Run2016G": 7575.824,
    "Run2016H": 8650.628,
    # hww muon periods
    "Run271036to275783": 6274.191,
    "Run275784to276500": 3426.131,
    "Run276501to276811": 3191.207,

    # 2017 - using approved normtag + re-reco golden JSON
    # ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt
    "Run2017B": 4793.970,
    "Run2017C": 9632.746,
    "Run2017D": 4247.793,
    "Run2017E": 9314.581,
    "Run2017F": 13539.905,

    # 2018 - using approved normtag + re-reco golden JSON
    # ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt
    "Run2018A": 14027.614,
    "Run2018B": 7066.552,
    "Run2018C": 6898.817,
    "Run2018D": 31747.582,
    # before/after muon HLT update (during 2018A)
    "Run315264to316360": 8928.970,
    "Run316361to325175": 50789.746
}


# TODO maybe move this elsewhere
binningVariables_nano = {
    "Eta": lambda obj: obj.eta,
    "AbsEta": lambda obj: op.abs(obj.eta),
    "ClusEta": lambda el: el.eta + el.deltaEtaSC,
    "AbsClusEta": lambda el: op.abs(el.eta + el.deltaEtaSC),
    "Pt": lambda obj: obj.pt
}


def getBinningVarNames(jsonpath):
    import json
    with open(jsonpath) as jsf:
        cont = json.load(jsf)
    return tuple(cont["variables"])


class BinningParameters:
    def __init__(self, binningVars):
        self.binningVars = binningVars

    def __call__(self, obj):
        return op.construct(
            "Parameters",
            (op.initList(
                "std::initializer_list<Parameters::value_type::value_type>",
                "Parameters::value_type::value_type", (
                    op.initList(
                        "Parameters::value_type::value_type", "float",
                        (op.extVar("int", "BinningVariable::{}".format(
                            bvNm.replace("ClusEta", "Eta"))), bv(obj)))
                    for bvNm, bv in self.binningVars.items())),)
        )


def getBinningParameters(bVarNames, isElectron=False, moreVars=None, paramDefs=None):
    if isElectron:
        bVarNames = [k.replace("Eta", "ClusEta") for k in bVarNames]
    theDict = dict(paramDefs) if paramDefs else {}
    if moreVars:
        theDict.update(moreVars)
    return BinningParameters({k: theDict[k] for k in bVarNames})


class ScaleFactor:
    def __init__(self, cppDef=None, args=None, iface="ILeptonScaleFactor",
                 systName=None, seedFun=None, defineOnFirstUse=True):
        self._cppDef = cppDef
        self._args = args
        self.sfOp = op.define(iface, cppDef)
        self._systName = systName
        self._seedFun = seedFun
        self.defineOnFirstUse = defineOnFirstUse

    def __call__(self, obj):
        args = list(a(obj) for a in self._args)
        if self._seedFun:
            args.append(self._seedFun(obj))
        expr = self.sfOp.get(*(args + [op.extVar("int", "Nominal")]))
        if self._systName:
            expr = op.systematic(
                expr, name=self._systName,
                up=self.sfOp.get(*(args + [op.extVar("int", "Up")])),
                down=self.sfOp.get(*(args + [op.extVar("int", "Down")])))
        if self.defineOnFirstUse:
            expr = op.defineOnFirstUse(expr)
        return expr


def get_scalefactor(
        objType, key, combine=None, additionalVariables=None, sfLib=None, paramDefs=None,
        lumiPerPeriod=None, periods=None, getFlavour=None, isElectron=False,
        systName=None, seedFun=None, defineOnFirstUse=True):
    """ Construct a scalefactor callable

    .. warning::
        This function is deprecated. Use `correctionlib <https://cms-nanoaod.github.io/correctionlib/>`_ and
        :py:func:`~bamboo.scalefactors.get_correction` instead.

    :param objType: object type: ``"lepton"``, ``"dilepton"``, or ``"jet"``
    :param key: key in ``sfLib`` (or tuple of keys, in case of a nested dictionary),
        or JSON path (or list thereof) if ``sfLib`` is not specified
    :param sfLib: dictionary (or nested dictionary) of scale factors.
        A scale factor entry is either a path to a JSON file, or a list of pairs ``(periods, path)``,
        where ``periods`` is a list of periods found in ``lumiPerPeriod`` and ``path`` is a path
        to the JSON file with the scale factors corresponding to those run periods.
    :param combine: combination strategy for combining different run periods
        (``"weight"`` or ``"sample"``)
    :param paramDefs: dictionary of binning variable definitions (name to callable)
    :param additionalVariables: additional binning variable definitions (TODO: remove)
    :param lumiPerPeriod: alternative definitions and relative weights of run periods
    :param periods: Only combine scale factors for those periods
    :param isElectron: if True, will use supercluster eta instead of eta (for ``"lepton"`` type only)
        (TODO: find a better way of doing that)
    :param systName: name of the associated systematic nuisance parameter
    :param seedFun: (only when combining scalefactor by sampling)
        callable to get a random generator seed for an object, e.g. ``lambda l : l.idx+42``
    :param defineOnFirstUse: wrap with :py:func:`~bamboo.treefunctions.defineOnFirstUse`
        (to define as a column and reuse afterwards),
        this is enabled by default since it is usually more efficient

    :returns: a callable that takes ``(object, variation="Nominal")``
        and returns a floating-point number proxy
    """

    logger.warning("get_scalefactor() is deprecated! Use correctionlib and get_correction() instead")

    #
    # Interpret args, get defaults etc.
    #
    if sfLib is None:
        config = key
    elif isinstance(key, tuple):
        # interpret key=("a", "b") as ...["a"]["b"]
        config = sfLib[key[0]]
        for idx in range(1, len(key)):
            config = config[key[idx]]
    else:
        config = sfLib[key]

    if combine is not None:
        combPrefix = {
            "weight": "W",
            "sample": "Smp"
        }.get(combine, "W")
        if combine == "sample" and not seedFun:
            raise ValueError(
                "If combining by sampling, a seed function needs to be passed to get_scalefactor")

    if getFlavour is None:
        def getFlavour(j):
            return j.hadronFlavour
    getFlavour = partial(lambda getter, j: op.extMethod(
        "IJetScaleFactor::get_flavour")(getter(j)), getFlavour)

    if lumiPerPeriod:
        lumiPerPeriod_default.update(lumiPerPeriod)
    lumiPerPeriod = lumiPerPeriod_default
    if periods is None:
        periods = lumiPerPeriod.keys()

    #
    # Construct scalefactors
    #
    if objType == "lepton":
        iface = "ILeptonScaleFactor"
        if isinstance(config, str):
            return ScaleFactor(
                cppDef=f'const ScaleFactor <<name>>{{"{config}"}};',
                args=(getBinningParameters(
                    getBinningVarNames(config), isElectron=isElectron,
                    moreVars=additionalVariables, paramDefs=paramDefs),),
                iface=iface, systName=systName, defineOnFirstUse=defineOnFirstUse)
        else:
            if combPrefix == "":
                raise ValueError("A combination mode needs to be specified for this scale factor")
            selConfigs = list(
                filter(
                    (lambda elm: elm[0] != 0.),  # only keep those with nonzero lumi
                    ((sum(lumiPerPeriod[ier] for ier in eras if ier in periods), path)
                        for eras, path in config if any(ier in periods for ier in eras))
                ))
            if len(selConfigs) < 1:
                raise RuntimeError(
                    "Zero period configs selected for config {} with periods {}".format(
                        ", ".join(f"({list(eras)} : {path})" for eras, path in config),
                        list(periods)))
            elif len(selConfigs) == 1:
                return ScaleFactor(
                    cppDef=f'const ScaleFactor <<name>>{{"{selConfigs[0][1]}"}};',
                    args=(getBinningParameters(
                        getBinningVarNames(selConfigs[0][1]), isElectron=isElectron,
                        moreVars=additionalVariables, paramDefs=paramDefs),),
                    iface=iface, systName=systName, defineOnFirstUse=defineOnFirstUse)
            else:
                bVarNames = set(chain.from_iterable(getBinningVarNames(iPth)
                                                    for iWgt, iPth in selConfigs))
                return ScaleFactor(
                    cppDef=(
                        'std::unique_ptr<{iface}> tmpSFs_<<name>>[] = {{ {0} }};\n'.format(", ".join(
                            f'std::make_unique<ScaleFactor>("{path}")'
                            for wgt, path in selConfigs), iface=iface)
                        + 'const {cmb}ScaleFactor <<name>>{{ {{ {0} }}, '.format(
                            ", ".join(f"{wgt:e}" for wgt, path in selConfigs), cmb=combPrefix)
                        + (f'std::vector<std::unique_ptr<{iface}>>{{'
                           f'std::make_move_iterator(std::begin(tmpSFs_<<name>>)), '
                           f'std::make_move_iterator(std::end(tmpSFs_<<name>>))}} }};')
                    ),
                    args=(getBinningParameters(
                        bVarNames, isElectron=isElectron,
                        moreVars=additionalVariables, paramDefs=paramDefs),),
                    iface=iface, systName=systName,
                    seedFun=(seedFun if combine == "sample" else None),
                    defineOnFirstUse=defineOnFirstUse
                )
    elif objType == "dilepton":
        iface = "IDiLeptonScaleFactor"
        if isinstance(config, tuple) and len(config) == 4:
            if not all(isinstance(iCfg, str) for iCfg in config):
                raise TypeError(
                    "Config for dilepton scale factor should be quadruplet of paths "
                    f"or list of weights and triplets, found {config}")

            return ScaleFactor(
                cppDef="const DiLeptonFromLegsScaleFactor <<name>>{{{0}}};".format(", ".join(
                    f'std::make_unique<ScaleFactor>("{leplepCfg}")' for leplepCfg in config)),
                args=[(lambda bp: (lambda ll: bp(ll[0])))(
                    getBinningParameters(
                        set(chain(getBinningVarNames(config[0]), getBinningVarNames(config[1]))),
                        moreVars=additionalVariables, paramDefs=paramDefs)),
                      (lambda bp: (lambda ll: bp(ll[1])))(
                          getBinningParameters(
                              set(chain(getBinningVarNames(config[2]), getBinningVarNames(config[3]))),
                              moreVars=additionalVariables, paramDefs=paramDefs))],
                iface=iface, systName=systName, defineOnFirstUse=defineOnFirstUse)
        else:
            raise NotImplementedError("Still to do this part")
    elif objType == "jet":
        iface = "IJetScaleFactor"
        if isinstance(config, tuple) and len(config) == 3:
            if not all(isinstance(iCfg, str) for iCfg in config):
                raise TypeError(
                    f"Config for b-tagging should be triplet of paths "
                    "or list of weights and triplets, found {config}")
            else:
                bVarNames = set(chain.from_iterable(getBinningVarNames(iCfg) for iCfg in config))
                return ScaleFactor(
                    cppDef='const BTaggingScaleFactor <<name>>{{{0}}};'.format(
                        ", ".join(f'"{iCfg}"' for iCfg in config)),
                    args=(getBinningParameters(
                        bVarNames, moreVars=additionalVariables,
                        paramDefs=paramDefs), getFlavour),
                    iface=iface, systName=systName, defineOnFirstUse=defineOnFirstUse)
        else:
            if not (all((isinstance(iCfg, tuple) and len(iCfg) == 3 and all(
                    isinstance(iPth, str) for iPth in iCfg)) for iCfg in config)):
                raise TypeError(
                    "Config for b-tagging should be triplet of paths "
                    f"or list of weights and triplets, found {config}")
            else:
                if combPrefix == "":
                    raise ValueError("A combination mode needs to be specified for this scale factor")
                selConfigs = list(
                    filter(
                        (lambda elm: elm[0] != 0.),  # only keep those with nonzero lumi
                        ((sum(lumiPerPeriod[ier] for ier in eras if ier in periods), path)
                            for eras, path in config if any(ier in periods for ier in eras))))
                if len(selConfigs) < 1:
                    raise RuntimeError("Zero configs")
                elif len(selConfigs) == 1:
                    bVarNames = set(chain.from_iterable(getBinningVarNames(iCfg) for iCfg in selConfigs[0]))
                    return ScaleFactor(
                        cppDef='const BTaggingScaleFactor <<name>>{{{0}}};'.format(
                            ", ".join(f'"{iCfg}"' for iCfg in selConfigs[0])),
                        args=(getBinningParameters(
                            bVarNames, moreVars=additionalVariables, paramDefs=paramDefs), getFlavour),
                        iface=iface, systName=systName, defineOnFirstUse=defineOnFirstUse)
                else:
                    bVarNames = set(chain.from_iterable(getBinningVarNames(iPth)
                                    for iWgt, paths in selConfigs for iPth in paths))
                    return ScaleFactor(
                        cppDef=('std::unique_ptr<{iface}> tmpSFs_<<name>>[] = {{ {0} }};\n'.format(", ".join(
                            'std::make_unique<BTaggingScaleFactor>({})'.format(
                                ", ".join(f'"{iPth}"' for iPth in paths))
                            for wgt, paths in selConfigs), iface=iface)
                            + 'const {cmb}ScaleFactor <<name>>{{ {{ {0} }}, '.format(
                                ", ".join(f"{wgt:e}" for wgt, paths in selConfigs), cmb=combPrefix)
                            + (f'std::vector<std::unique_ptr<{iface}>>{{'
                               f'std::make_move_iterator(std::begin(tmpSFs_<<name>>)), '
                               f'std::make_move_iterator(std::end(tmpSFs_<<name>>))}} }};')
                        ),
                        arg=(getBinningParameters(
                            bVarNames, moreVars=additionalVariables, paramDefs=paramDefs), getFlavour),
                        iface=iface, systName=systName,
                        seedFun=(seedFun if combine == "sample" else None),
                        defineOnFirstUse=defineOnFirstUse)
    else:
        raise ValueError(f"Unknown object type: {objType}")


class BtagSF:
    """ Helper for b- and c-tagging scalefactors using the BTV POG reader """
    def _nano_getPt(jet):
        import bamboo.treeproxies as _tp
        if isinstance(jet._parent, _tp.AltCollectionProxy):
            bs = jet._parent._base
            return bs.brMap["pt"].wrapped.result[jet.idx]  # use nominal always
        else:
            return jet.pt

    def _nano_getEta(jet):
        import bamboo.treefunctions as op
        return op.abs(jet.eta)

    def _nano_getJetFlavour(jet):
        import bamboo.treefunctions as op
        return op.extMethod("BTagEntry::jetFlavourFromHadronFlavour")(jet.hadronFlavour)

    def _translate_btagSFVarToJECVar(btagVarName, prefix="btagSF_"):
        if btagVarName.startswith("up_jes") or btagVarName.startswith("down_jes"):
            if btagVarName.endswith("_jes"):
                return "jesTotal{}".format(btagVarName.split("_jes")[0])
            return "jes{1}{0}".format(*btagVarName.split("_jes"))
        elif btagVarName.startswith("up_") or btagVarName.startswith("down_"):
            tk = btagVarName.split("_")
            return "".join((prefix, "_".join(tk[1:]), tk[0]))
        elif btagVarName in ("up", "down"):
            return "".join((prefix, btagVarName))
        else:
            return btagVarName

    def translateFixedWPCorrelation(btagVarName, prefix="btagSF", year=None):
        if btagVarName.endswith("_correlated"):
            rest = "_".join(btagVarName.split("_")[:-1])
            return f"{prefix}{year}{rest}"
        elif btagVarName.endswith("_uncorrelated"):
            rest = "_".join(btagVarName.split("_")[:-1])
            return f"{prefix}{rest}"
        else:
            return f"{prefix}{btagVarName}"

    def __init__(
            self, taggerName, csvFileName, wp=None, sysType="central", otherSysTypes=None,
            measurementType=None, getters=None, jesTranslate=None, sel=None, uName=None):
        """
        Declare a BTagCalibration (if needed) and BTagCalibrationReader (unique, based on ``uName``),
            and decorate for evaluation

        .. warning::
            This function is deprecated.
            Use `correctionlib <https://cms-nanoaod.github.io/correctionlib/>`_ and
            helpers in :py:mod:`~bamboo.scalefactors` instead.

        :param taggerName: first argument for ``BTagCalibration``
        :param csvFileName: name of the CSV file with scalefactors
        :param wp: working point (used as ``BTagEntry::OP_{wp.upper()}``)
        :param sysType: nominal value systematic type (``"central"``, by default)
        :param otherSysTypes: other systematic types to load in the reader
        :param measurementType: dictionary with measurement type per true flavour (B, C, and UDSG),
            or a string if the same for all (if not specified,
            ``"comb"`` will be used for b- and c-jets, and ``incl`` for light-flavour jets)
        :param getters: dictionary of methods to get the kinematics and classifier for a jet
            (the keys ``Pt``, ``Eta``, ``JetFlavour``, and ``Discri`` are used.
            For the former three, the defaults are for NanoAOD)
        :param jesTranslate: translation function for JEC systematic variations,
            from the names in the CSV file to those used for the jets
            (the default should work for on-the-fly corrections)
        :param sel: a selection in the current graph
        :param uName: unique name, to declare the reader (e.g. sample name)
        """
        logger.warning("BtagSF is deprecated! Use correctionlib and other bamboo helpers instead")

        if otherSysTypes is None:
            otherSysTypes = []
        self.nomName = sysType
        self.varNames = otherSysTypes
        if measurementType is None:  # BTV recommendation for b-tagging with fixed working points
            measurementType = {"B": "comb", "C": "comb", "UDSG": "incl"}
        elif isinstance(measurementType, str):  # if string, use it for all
            measurementType = {fl: measurementType for fl in ("B", "C", "UDSG")}
        calibName = sel._fbe.symbol(
            f'const BTagCalibration <<name>>{{"{taggerName}", "{csvFileName}"}};',
            nameHint=f"bTagCalib_{taggerName}")
        readerName = sel._fbe.symbol(
            'BTagCalibrationReader <<name>>{{BTagEntry::OP_{0}, "{1}", {{ {2} }} }}; // for {3}'.format(
                wp.upper(), sysType, ", ".join(f'"{sv}"' for sv in otherSysTypes), uName),
            nameHint="bTagReader_{}".format("".join(c for c in uName if c.isalnum())))
        from bamboo.root import gbl
        calibHandle = getattr(gbl, calibName)
        readerHandle = getattr(gbl, readerName)
        for flav, measType in measurementType.items():
            readerHandle.load(calibHandle, getattr(gbl.BTagEntry, f"FLAV_{flav}"), measType)
        import bamboo.treefunctions as op
        self.reader = op.extVar("BTagCalibrationReader", readerName)
        if getters is None:
            self.getters = [BtagSF._nano_getJetFlavour, BtagSF._nano_getEta, BtagSF._nano_getPt]
        else:
            self.getters = [
                getters.get("JetFlavour", BtagSF._nano_getJetFlavour),
                getters.get("Eta", BtagSF._nano_getEta),
                getters.get("Pt", BtagSF._nano_getPt)]
            if "Discri" in getters:
                self.getters.append(getters["Discri"])
        self.jesTranslate = jesTranslate if jesTranslate is not None else BtagSF._translate_btagSFVarToJECVar

    def _evalFor(self, var, jet):
        import bamboo.treefunctions as op
        varName_p = op._to.Parameter("std::string", f'"{var}"').result
        return self.reader.eval_auto_bounds(varName_p, *(gtr(jet) for gtr in self.getters))

    def __call__(self, jet, nomVar=None, systVars=None):
        """
        Evaluate the scalefactor for a jet

        Please note that this only gives the applicable scalefactor:
        to obtain the event weight one of the recipes in the
        `POG twiki <https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagSFMethods>`_
        should be used.

        By default the nominal and systematic variations are taken from
        the :py:class:`bamboo.scalefactors.BtagSF` instance, but they can be
        overriden with the ``nomVar`` and ``systVars`` keyword arguments.
        Please note that when using split uncertainties (e.g. for the reshaping
        method) some uncertainties only apply to specific jet flavours
        (e.g. c-jets) and the csv file contains zeroes for the other flavours.
        Then the user code should check the jet flavours, and call this method
        with the appropriate list of variations for each.
        """
        import bamboo.treefunctions as op
        nom = self._evalFor((nomVar if nomVar is not None else self.nomName), jet)
        if systVars is not None and not systVars:  # empty, no systematic
            return nom
        else:
            if systVars is not None:
                if any(sv not in self.varNames for sv in systVars):
                    logger.error(
                        "B-tag SF systematic variations {} were not loaded, skipping".format(
                            ", ".join(sv for sv in systVars if sv not in self.varNames)))
                    systVars = [sv for sv in systVars if sv in self.varNames]
            else:
                systVars = self.varNames
            return op.systematic(nom, **{self.jesTranslate(var): self._evalFor(var, jet) for var in systVars})


class CorrectionHelper:
    def __init__(
            self, corrOp, inputs, params, systParam=None,
            systNomName="nominal", systVariations=None, defineOnFirstUse=True):
        self.corrOp = corrOp
        self.inputs = inputs
        self.params = params
        self.systParam = systParam
        self.systNomName = systNomName
        self.systVariations = systVariations
        self.defineOnFirstUse = defineOnFirstUse

    @staticmethod
    def makeEvalArg(args):
        return op.initList(
            "std::vector<correction::Variable::Type>",
            "correction::Variable::Type",
            args)

    def __call__(self, obj):
        args = []
        iSyst = None
        for pName in self.inputs:
            if pName == self.systParam:
                iSyst = self.inputs.index(self.systParam)
                args.append(op._tp.makeConst(self.systNomName, "std::string"))
            else:
                p = self.params[pName]
                if callable(p):
                    args.append(p(obj))
                else:
                    args.append(p)
        expr = self.corrOp.evaluate(CorrectionHelper.makeEvalArg(args))
        if self.systVariations:
            variations = {}
            for vName, vCatIndex in self.systVariations.items():
                vArgs = list(args)
                vArgs[iSyst] = op._tp.makeConst(vCatIndex, "std::string")
                vExpr = self.corrOp.evaluate(CorrectionHelper.makeEvalArg(vArgs))
                variations[vName] = vExpr
            expr = op.systematic(expr, **variations)
        if self.defineOnFirstUse:
            expr = op.defineOnFirstUse(expr)
        return expr


_loadedCorrectionSets = {}


class CorrectionInputError(Exception):
    pass


def get_correction(
        path, correction, params=None, systParam=None, systNomName="nominal",
        systVariations=None, systName=None, defineOnFirstUse=True, sel=None):
    """
    Load a correction from a CMS JSON file

    The JSON file is parsed with `correctionlib <https://github.com/cms-nanoAOD/correctionlib>`_.
    The contents and structure of a JSON file can be checked with the
    ``correction`` script, e.g. ``correction summary sf.json``

    :param path: JSON file path
    :param correction: name of the correction inside ``CorrectionSet`` in the JSON file
    :param params: parameter definitions, a dictionary of values or functions
    :param systParam: name of the parameter (category axis) to use for systematic variations
    :param systNomName: name of the systematic category axis to use as nominal
    :param systVariations: systematic variations list or ``{variation: name_in_json}``
    :param systName: systematic uncertainty name (to prepend to names, if 'up' and 'down')
    :param defineOnFirstUse: wrap with :py:func:`~bamboo.treefunctions.defineOnFirstUse`
        (to define as a column and reuse afterwards),
        this is enabled by default since it is usually more efficient
    :param sel: a selection in the current graph (only used to retrieve a pointer to the backend)

    :returns: a callable that takes ``(object)`` and returns the correction
        (with systematic variations, if present and unless a specific variation is requested)
        obtained by evaluating the remaining parameters with the object

    :Example:

    >>> elIDSF = get_correction("EGM_POG_SF_UL.json", "electron_cutbased_looseID",
    >>>     params={"pt": lambda el : el.pt, "eta": lambda el : el.eta},
    >>>     systParam="weight", systNomName="nominal", systName="elID", systVariations=("up", "down")
    >>>     )
    >>> looseEl = op.select(t.Electron, lambda el : el.looseId)
    >>> withDiEl = noSel.refine("withDiEl",
    >>>     cut=(op.rng_len(looseEl) >= 2),
    >>>     weight=[ elIDSF(looseEl[0]), elIDSF(looseEl[1]) ]
    >>>     )
    """
    from .root import loadcorrectionlib
    be = sel._fbe  # backend reference
    loadcorrectionlib(backend=be)
    # TODO real path (but not abs), expanduser?
    if path not in _loadedCorrectionSets:
        _loadedCorrectionSets[path] = (be.symbol(
            f'auto <<name>> = correction::CorrectionSet::from_file("{path}");'), {})
    corrSetName, loadedCorrs = _loadedCorrectionSets[path]
    if correction not in loadedCorrs:
        loadedCorrs[correction] = be.symbol(f'auto <<name>> = {corrSetName}->at("{correction}");')
    corrName = loadedCorrs[correction]
    corrObj = op.extVar("correction::Correction*", corrName)
    from .root import gbl
    corrHandle = getattr(gbl, corrName)
    if systVariations and not isinstance(systVariations, dict):
        systVars = {}
        for vn in systVariations:
            if vn.lower() in ("up", "down") and systName:
                systVars[f"{systName}{vn}"] = vn
            else:
                if systName:
                    logger.warning(
                        "Systematic name given, and variation not up or down, "
                        f"using only variation name '{vn}'")
                systVars[vn] = vn
        systVariations = systVars
    corrInputs = [p.name() for p in corrHandle.inputs()]
    if params is not None:
        missingInputs = set(corrInputs) - set(params.keys())
        if systParam:
            missingInputs.remove(systParam)
        if missingInputs:
            raise CorrectionInputError(
                f"For correction {correction} in {path}, "
                f"the following inputs are missing: {missingInputs}")
        extraInputs = set(params.keys()) - set(corrInputs)
        if extraInputs:
            raise CorrectionInputError(
                f"For correction {correction} in {path}, "
                f"the following inputs are not expected: {extraInputs}")
    return CorrectionHelper(
        corrObj,
        corrInputs,
        params=params,
        systParam=systParam,
        systNomName=systNomName,
        systVariations=systVariations,
        defineOnFirstUse=defineOnFirstUse
    )


def get_bTagSF_fixWP(json_path, tagger, wp, flavour, sel, jet_pt_variation=None, heavy_method="comb",
                     syst_prefix="btagSF_fixWP_", decorr_wps=False, decorr_eras=False, era=None,
                     full_scheme=False, syst_mapping=None, defineOnFirstUse=True):
    """Build correction evaluator for fixed working point b-tagging scale factors

    Loads the b-tagging scale factors as correction object from the JSON file,
    configures the systematic variations, and returns a callable that
    can be evaluated on a jet to return the scale factor.

    :param json_path: JSON file path
    :param tagger: name of the tagger inside the JSON (not the same as in the event!)
    :param wp: working point of the tagger (`"L"`, `"M"`, `"T"`)
    :param flavour: hadron flavour of the jet (`0`, `4`, `5`)
    :param sel: a selection in the current graph (only used to retrieve a pointer to the backend)
    :param jet_pt_variation: if specified, only use that specific systematic variation (e.g. the `nominal`)
        of the jet pt to evaluate the scale factors. By default, the scale factors are evaluated for
        each variation.
    :param heavy_method: B-tagging measurement method for heavy-flavour jets (`"comb"` or `"mujets"`).
        For light jets, there is only the `"incl"` method.
    :param syst_prefix: Prefix to prepend to the name of all resulting the b-tagging systematic variations.
        Variations for light or heavy jets will be prefixed resp.
        by `{syst_prefix}light` or `{syst_prefix}heavy` (unless the full scheme is used).
    :param decorr_wps: If `True`, insert the working point into the systematic name for
        the uncorrelated/statistical component. Otherwise, all working points will be taken as fully
        correlated when using several in the analysis.
    :param decorr_eras: If `True`, use the scale factor uncertainties split into "uncorrelated"
        and "correlated" parts, and insert the `era` name into the variation names.
        If `False`, only use the total scale factor uncertainties (not split).
    :param era: Name of era, used in the name of systematic variations if one of `decorr_eras`
        or `full_scheme` is `True`.
    :param full_scheme: If `True`, use split uncertainty sources as specified in the `full_scheme` argument
    :param syst_mapping: Dictionary used to list the systematics to consider, and
        to map the naming of the full-scheme b-tagging uncertainties
        to variations defined elsewhere in the analysis, for varying them together when needed
        (see example below).
    :param defineOnFirstUse: see description in :py:func:`~bamboo.scalefactors.get_correction`

    :returns: a callable that takes a jet and returns the correction
        (with systematic variations as configured here)
        obtained by evaluating the b-tagging scale factors on the jet

    :Example:

    >>> btvSF_b = get_bTagSF_fixWP("btv.json", "deepJet", "M", 5, sel, syst_prefix="btagSF_",
    >>>                            era="2018UL", full_scheme=True,
    >>>                            syst_mapping={
    >>>                                "pileup": "pileup",
    >>>                                "type3": None,
    >>>                                "jer0": "jer",
    >>>                                "jer1": "jer"
    >>>                             })

    Will result in the following systematic uncertainties:
        - `btagSF_statistic_2018UL{up/down}`: mapped to `{up/down}_statistic` in the JSON
        - `btagSF_pileup{up/down}`: mapped to `{up/down}_pileup` in the JSON, and correlated
            with the `pileup{up/down}` variations in the analysis
        - `btagSF_type3{up/down}`: mapped to `{up/down}_type3` in the JSON
        - `btagSF_jer0{up/down}`: mapped to `{up/down}_jer` in the JSON, and correlated
            with the `jer0{up/down}` variations in the analysis
        - `btagSF_jer1{up/down}`: mapped to `{up/down}_jer` in the JSON, and correlated
            with the `jer1{up/down}` variations in the analysis

    >>> btvSF_b = get_bTagSF_fixWP("btv.json", "deepJet", "M", 5, sel, syst_prefix="btagSF_",
    >>>                            era="2018UL", decorr_wps=True, decorr_eras=True)

    Will result in the following systematic uncertainties:
        - `btagSF_heavy_M_2018UL{up/down}`: mapped to `{up/down}_uncorrelated` in the JSON
        - `btagSF_heavy{up/down}`: mapped to `{up/down}_correlated` in the JSON
    """
    if not era and (decorr_eras or full_scheme):
        raise RuntimeError("Need to specify an era if the nuisances are to be decorrelated across eras, "
                           "or if the full uncertainty scheme is used")
    params = {
        "pt": lambda j: op.forSystematicVariation(j.pt, jet_pt_variation) if jet_pt_variation else j.pt,
        "abseta": lambda j: op.abs(j.eta), "working_point": wp, "flavor": flavour
    }
    systName = syst_prefix + ("light" if flavour == 0 else "heavy")
    wpDecorrTag = f"_{wp}" if decorr_wps else ""
    systVariations = {}
    for d in ("up", "down"):
        if not decorr_eras and not full_scheme:
            systVariations[f"{systName}{d}"] = d
        elif decorr_eras and (not full_scheme or flavour == 0):
            systVariations[f"{systName}{d}"] = f"{d}_correlated"
            systVariations[f"{systName}{wpDecorrTag}_{era}{d}"] = f"{d}_uncorrelated"
        elif full_scheme and flavour > 0:
            systVariations[f"{syst_prefix}statistic{wpDecorrTag}_{era}{d}"] = f"{d}_statistic"
            for var, varBTV in syst_mapping.items():
                if varBTV is None:
                    systVariations[f"{syst_prefix}{var}{d}"] = f"{d}_{var}"
                else:
                    systVariations[f"{var}{d}"] = f"{d}_{varBTV}"

    if tagger == "deepCSV_subjet":
        method = "incl" if flavour == 0 else "lt"
        params["method"] = method
        taggerStr = tagger
    else:
        method = "incl" if flavour == 0 else heavy_method
        taggerStr = f"{tagger}_{method}"

    return get_correction(json_path, taggerStr, params=params,
                          systParam="systematic", systNomName="central",
                          systVariations=systVariations, sel=sel, defineOnFirstUse=defineOnFirstUse)


def makeBtagWeightMeth1a(jets, tagger, wps, workingPoints, sfGetter, effGetters):
    """Construct the full event weight based on b-tagging scale factors
    (fixed working point) and efficiencies

    Combines the b-tagging scale factors and MC efficiencies for fixed working points
    into the event weight needed to correct the simulation (the event weight can then
    directly be passed to a selection). The weight is computed according to
    `Method 1a <https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagSFMethods#1a_Event_reweighting_using_scale>`_,  # noqa: B950
    with support for several working points.

    While the scale factors can be loaded from the POG-provided JSON files,
    the efficiencies need to be computed by the analyzers.

    :param jets: the jet collection in the event
    :param tagger: the name of the tagger in the event
    :param wps: a list of working points for which the b tagging must be corrected,
        e.g. `["L", "T"]` for computing the weight using scale factors for the `L` and `T`
        working points. Note: always provide the working points in increasing order of "tightness"!
    :param workingPoints: a dictionary providing the working point value for the discriminator
    :param sfGetter: a callable that takes the working point (`str`) and the hadron flavour (`int`)
        and returns the correction object for the b-tagging scale factors of that working point
        and jet flavour (i.e., itself a callable that takes the jet and returns the scale factor).
        See :py:meth:`bamboo.scalefactors.get_bTagSF_fixWP`.
    :param effGetters: a dictionary with keys = working points and values = callables that can be evaluated
        on a jet and return the b-tagging efficiency for that working point. Typically,
        these would be correction objects parameterized using the jet pt, eta and hadron flavour.

    :returns: a weight proxy (with all systematic variations configured in the scale factors)

    :Example:

    >>> btvSF = lambda wp, flav: get_bTagSF_fixWP("btv.json", "deepJet", wp, flav, ...)
    >>> btvEff = {"M": get_correction("my_btag_eff.json", ...)}
    >>> btvWeight = makeBtagWeightMeth1a(tree.jet, "btagDeepFlavB", ["M"], {"M": 0.2783},
    >>>                                  btvSF, btvEff)
    >>> sel_btag = sel.refine("btag", cut=..., weight=btvWeight)
    """
    # Functions selecting the right SF depending on jet flavour
    # The flavour can't be passed as parameter to correctionlib because the
    # uncertainties depend on it.
    bTagSFs = {}
    for wp in wps:
        bTagSFs[wp] = lambda j, wp_=wp: op.multiSwitch(
            (j.hadronFlavour == 5, sfGetter(wp_, 5)(j)),
            (j.hadronFlavour == 4, sfGetter(wp_, 4)(j)),
            sfGetter(wp_, 0)(j))

    wFail = op.extMethod("scalefactorWeightForFailingObject", returnType="double")

    def jet_SF(j):
        factors = []
        # [L,M,T] -> (if discr >= T, then: )
        tightest = wps[-1]
        factors.append((getattr(j, tagger) >= workingPoints[tightest], bTagSFs[tightest](j)))
        # [L,M,T] -> (elif discr >= M, then: ), (elif discr >= L, then: )
        for i in range(len(wps) - 1, 0, -1):
            tighter = wps[i]
            looser = wps[i - 1]
            factors.append((getattr(j, tagger) >= workingPoints[looser],
                            wFail(bTagSFs[tighter](j), effGetters[tighter](j),
                                  bTagSFs[looser](j), effGetters[looser](j))))
        # [L,M,T] -> (else: )
        loosest = wps[0]
        factors.append(wFail(bTagSFs[loosest](j), effGetters[loosest](j)))
        return op.multiSwitch(*factors)

    # method 1a: product over jets, factors depend on discriminator value
    return op.rng_product(jets, jet_SF)


def get_bTagSF_itFit(json_path, tagger_json, tagger_jet, flavour, sel, jet_pt_variation=None,
                     syst_prefix="btagSF_shape_",
                     decorr_eras=False, era=None, syst_mapping=None, defineOnFirstUse=True):
    """Build correction evaluator for continuous (iterativeFit) b-tagging scale factors

    Loads the b-tagging scale factors as correction object from the JSON file,
    configures the systematic variations, and returns a callable that
    can be evaluated on a jet to return the scale factor.

    :param json_path: JSON file path
    :param tagger_json: name of the tagger inside the JSON
    :param tagger_jet: name of the tagger in the tree
    :param flavour: hadron flavour of the jet (`0`, `4`, `5`)
    :param sel: a selection in the current graph (only used to retrieve a pointer to the backend)
    :param jet_pt_variation: see description in :py:func:`~bamboo.scalefactors.get_bTagSF_fixWP`
    :param syst_prefix: Prefix to prepend to the name of all resulting the b-tagging systematic variations.
    :param decorr_eras: If `True`, insert the era into the variation name for statistical uncertainties
    :param era: Name of era, used in the name of systematic variations if `decorr_eras` is `True`
    :param syst_mapping: see description in :py:func:`~bamboo.scalefactors.get_bTagSF_fixWP`,
        with the difference that here the "basic" (non-JES-related) variations are already included
        no matter what.
    :param defineOnFirstUse: see description in :py:func:`~bamboo.scalefactors.get_correction`

    :returns: a callable that takes a jet and returns the correction
        (with systematic variations as configured here)
        obtained by evaluating the b-tagging scale factors on the jet

    :Example:

    >>> btvSF_b = get_bTagSF_itFit("btv.json", "deepJet", "btagDeepFlavB", 5, sel, syst_prefix="btagSF_",
    >>>                            decorr_eras=True, era="2018UL",
    >>>                            syst_mapping={"jesTotal": "jes"})

    Will result in the following systematic uncertainties:
        - `btagSF_hfstats1_2018UL{up/down}`: mapped to `{up/down}_hfstats1` in the JSON
        - `btagSF_hfstats2_2018UL{up/down}`: mapped to `{up/down}_hfstats2` in the JSON
        - `btagSF_lfstats1_2018UL{up/down}`: mapped to `{up/down}_lfstats1` in the JSON
        - `btagSF_lfstats2_2018UL{up/down}`: mapped to `{up/down}_lfstats2` in the JSON
        - `btagSF_hf{up/down}`: mapped to `{up/down}_hf` in the JSON
        - `btagSF_lf{up/down}`: mapped to `{up/down}_lf` in the JSON
        - `btagSF_jesTotal{up/down}`: mapped to `{up/down}_jes` in the JSON, and correlated
            with the `jesTotal{up/down}` variations in the analysis

    (for c jets, the `hf` and `lf` variations are absent and replaced by `cferr1` and `cferr2`)
    """

    systListUnCorr = []
    if flavour == 4:
        systListCorr = ["cferr1", "cferr2"]
    else:
        systListCorr = ["hf", "lf"]
        statSyst = ["hfstats1", "hfstats2", "lfstats1", "lfstats2"]
        if decorr_eras:
            systListUnCorr = statSyst
        else:
            systListCorr += statSyst

    systVariations = {}
    for d in ("up", "down"):
        for var in systListCorr:
            systVariations[f"{syst_prefix}{var}{d}"] = f"{d}_{var}"
        for var in systListUnCorr:
            systVariations[f"{syst_prefix}{var}_{era}{d}"] = f"{d}_{var}"
        if syst_mapping is not None:
            for var, varBTV in syst_mapping.items():
                systVariations[f"{var}{d}"] = f"{d}_{varBTV}"

    params = {
        "pt": lambda j: op.forSystematicVariation(j.pt, jet_pt_variation) if jet_pt_variation else j.pt,
        "abseta": lambda j: op.abs(j.eta),
        "discriminant": lambda j: getattr(j, tagger_jet), "flavor": flavour
    }
    return get_correction(json_path, f"{tagger_json}_shape", params=params,
                          systParam="systematic", systNomName="central",
                          systVariations=systVariations, sel=sel, defineOnFirstUse=defineOnFirstUse)


def makeBtagWeightItFit(jets, sfGetter):
    """Construct the full event weight based on b-tagging scale factors (continous/iterativeFit)

    Combines the b-tagging scale factors into the event weight needed to correct the simulation
    (the event weight can then directly be passed to a selection),
    by making a product of the scale factors over all jets.
    See the `note <https://twiki.cern.ch/twiki/bin/view/CMS/BTagShapeCalibration>`_ about
    correcting the normalization when using these scale factors.

    :param jets: the jet collection in the event
    :param sfGetter: a callable that takes the the hadron flavour (`int`)
        and returns the correction object for the b-tagging scale factors of that jet flavour
        (i.e., itself a callable that takes the jet and returns the scale factor)
        See :py:meth:`bamboo.scalefactors.get_bTagSF_itFit`.

    :returns: a weight proxy (with all systematic variations configured in the scale factors)

    :Example:

    >>> btvSF = lambda flav: get_bTagSF_itFit("btv.json", "deepJet", "btagDeepFlavB", flav, ...)
    >>> btvWeight = makeBtagWeightItFit(tree.jet, btvSF)
    >>> sel_btag = sel.refine("btag", cut=..., weight=btvWeight)
    """
    # The flavour can't be passed as parameter to correctionlib because the
    # uncertainties depend on it.
    def bTagSF(j):
        return op.multiSwitch(
            (j.hadronFlavour == 5, sfGetter(5)(j)),
            (j.hadronFlavour == 4, sfGetter(4)(j)),
            sfGetter(0)(j))
    return op.rng_product(jets, bTagSF)
