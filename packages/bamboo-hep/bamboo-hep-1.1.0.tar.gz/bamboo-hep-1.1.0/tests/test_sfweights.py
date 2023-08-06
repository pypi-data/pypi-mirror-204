import os.path

import pytest

from helpers import isclose_float

testData = os.path.join(os.path.dirname(__file__), "data")


def makeParameters(**kwargs):
    """ Construct Parameters argument for BinnedValues """
    from bamboo.root import gbl, loadBambooExtensions
    loadBambooExtensions()
    gbl.BinningVariable  # somehow loads Pt, Eta etc.
    params = gbl.Parameters()
    for k, v in kwargs.items():
        params.set(getattr(gbl, k), v)
    return params


@pytest.fixture(scope="module")
def sf_leptonSingle():
    from bamboo.root import gbl, loadBambooExtensions
    loadBambooExtensions()
    gbl.SystVariation  # somehow loads Nominal etc.
    elSFJSON = os.path.join(testData, "Electron_EGamma_SF2D_loose_moriond17.json")
    return gbl.ScaleFactor(elSFJSON)


@pytest.fixture(scope="module")
def sf_btagSingle():
    from bamboo.root import gbl, loadBambooExtensions
    loadBambooExtensions()
    gbl.SystVariation  # somehow loads Nominal etc.
    lightJSON = os.path.join(testData, "BTagging_loose_lightjets_incl_DeepJet_2016Legacy.json")
    cjetJSON = os.path.join(testData, "BTagging_loose_cjets_comb_DeepJet_2016Legacy.json")
    bjetJSON = os.path.join(testData, "BTagging_loose_bjets_comb_DeepJet_2016Legacy.json")
    return gbl.BTaggingScaleFactor(lightJSON, cjetJSON, bjetJSON)


@pytest.fixture(scope="module")
def puWeight():
    from bamboo.root import gbl, loadBambooExtensions
    loadBambooExtensions()
    puWeightJSON = os.path.join(os.path.dirname(__file__), "data", "puweights.json")
    return gbl.ScaleFactor(puWeightJSON)


@pytest.fixture(scope="module")
def test_lepSingle_constructEval(sf_leptonSingle):
    from bamboo.root import gbl
    central = 0.9901639223098755
    error = 0.19609383660010074
    assert isclose_float(
        sf_leptonSingle.get(makeParameters(Pt=20., Eta=1.5), gbl.Nominal),
        central)
    assert isclose_float(
        sf_leptonSingle.get(makeParameters(Pt=20., Eta=1.5), gbl.Up),
        central + error)
    assert isclose_float(
        sf_leptonSingle.get(makeParameters(Pt=20., Eta=1.5), gbl.Down),
        central - error)


def test_btagSingle_constructEval(sf_btagSingle):
    from bamboo.root import gbl
    central = 1.0912339687347412
    error = 0.057828545570373535
    assert isclose_float(
        sf_btagSingle.get(
            makeParameters(Pt=50., Eta=1.5, BTagDiscri=.5),
            gbl.IJetScaleFactor.Light, gbl.Nominal),
        central)
    assert isclose_float(
        sf_btagSingle.get(
            makeParameters(Pt=50., Eta=1.5, BTagDiscri=.5),
            gbl.IJetScaleFactor.Light, gbl.Up),
        central + error)
    assert isclose_float(
        sf_btagSingle.get(
            makeParameters(Pt=50., Eta=1.5, BTagDiscri=.5),
            gbl.IJetScaleFactor.Light, gbl.Down),
        central - error)


def test_puWeight_constructEvalInRange(puWeight):
    from bamboo.root import gbl
    assert isclose_float(
        puWeight.get(makeParameters(NumTrueInteractions=20.5), gbl.Nominal),
        1.0656023337493363)


def test_puWeight_evalBinEdge(puWeight):
    from bamboo.root import gbl
    assert isclose_float(
        puWeight.get(makeParameters(NumTrueInteractions=20.), gbl.Nominal),
        1.0656023337493363)


def test_puWeight_evalOutOfRangeBelow(puWeight):
    from bamboo.root import gbl
    assert isclose_float(
        puWeight.get(makeParameters(NumTrueInteractions=-.5), gbl.Nominal),
        0.36607730074755906)


def test_puWeight_evalOutOfRangeAbove(puWeight):
    from bamboo.root import gbl
    assert isclose_float(
        puWeight.get(makeParameters(NumTrueInteractions=100.), gbl.Nominal),
        0.001723281482149061)
