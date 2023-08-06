import logging
import os.path

import pytest

logging.basicConfig(level=logging.DEBUG)

testData = os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture(scope="module")
def decoNano():
    from bamboo.root import gbl
    f = gbl.TFile.Open(os.path.join(testData, "DY_M50_2016.root"))
    tree = f.Get("Events")
    from bamboo.treedecorators import (decorateNanoAOD, NanoAODDescription,
                                       nanoRochesterCalc, nanoJetMETCalc)
    from bamboo.dataframebackend import DataframeBackend
    tup = decorateNanoAOD(tree, NanoAODDescription.get(
        "v5", year="2016", isMC=True, systVariations=[nanoRochesterCalc, nanoJetMETCalc]))
    be, noSel = DataframeBackend.create(tup)
    from bamboo.analysisutils import configureJets, configureType1MET, configureRochesterCorrection
    configureJets(tup._Jet, "AK4PFchs", isMC=True, backend=be)
    configureType1MET(tup._MET, jec="Summer16_07Aug2017_V11_MC", isMC=True, backend=be)
    configureRochesterCorrection(tup._Muon, os.path.join(testData, "RoccoR2016.txt"),
                                 isMC=True, backend=be)
    yield tup, noSel, be


def test(decoNano):
    # a somewhat realistic (but not very sensible) combination of selections and plots
    tup, noSel, be = decoNano
    noSel = noSel.refine("mcWeight", weight=tup.genWeight)
    from bamboo import treefunctions as op
    from bamboo.plots import Plot
    from bamboo.plots import EquidistantBinning as EqBin
    from bamboo.analysisutils import forceDefine
    from functools import partial
    plots = []
    electrons = op.select(tup.Electron, lambda ele: op.AND(
        ele.cutBased_Sum16 >= 3, ele.pt > 15., op.abs(ele.eta) < 2.4))
    muons = op.select(tup.Muon, lambda mu: op.AND(
        mu.pt > 10., op.abs(mu.eta) < 2.4, mu.mediumId, mu.pfRelIso04_all < 0.15))
    plots.append(Plot.make1D(
        "nElectrons", op.rng_len(electrons), noSel, EqBin(10, 0., 10.),
        title="Number of electrons", xTitle="N_{e}"))
    hasMuon = noSel.refine("hasMuon", cut=(op.rng_len(muons) > 0))
    plots.append(Plot.make1D(
        "hasMuon_leadMuPT", muons[0].pt, hasMuon, EqBin(50, 0., 100.),
        title="Leading muon PT", xTitle="p_{T}(mu_{1})"))
    for calcProd in tup._Jet.calcProds:
        forceDefine(calcProd, noSel)
    jets = op.select(tup.Jet, lambda j: op.AND(j.pt > 20., op.abs(j.eta) < 2.4, j.jetId & 2))
    cleanedJets = op.select(jets, lambda j: op.AND(
        op.NOT(op.rng_any(electrons, lambda ele: op.deltaR(j.p4, ele.p4) < 0.3)),
        op.NOT(op.rng_any(muons, lambda mu: op.deltaR(j.p4, mu.p4) < 0.3))))
    plots.append(Plot.make1D(
        "nCleanedJets", op.rng_len(cleanedJets), noSel, EqBin(10, 0., 10.),
        title="Number of cleaned jets", xTitle="N_{j}"))
    cleanedJetsByDeepFlav = op.sort(cleanedJets, lambda jet: jet.btagDeepFlavB)
    hasMuJ = hasMuon.refine(
        "hasMuonJ", cut=(op.rng_len(cleanedJets) > 0),
        weight=op.rng_product(cleanedJetsByDeepFlav, lambda jet: jet.btagDeepB))
    plots.append(Plot.make1D(
        "hasMuonJ_prodBTags", op.rng_product(cleanedJetsByDeepFlav, lambda jet: jet.btagDeepB),
        hasMuJ, EqBin(1, 0., 1.), title="Product of jet b-tags", xTitle="X"))
    plots.append(Plot.make1D(
        "cleanedjet_pt", op.map(cleanedJets, lambda j: j.pt), noSel,
        EqBin(30, 30., 730.), title="Jet p_{T} (GeV)"))
    muRecoilJets = op.select(cleanedJets,
                             partial((lambda l, j: op.deltaR(l.p4, j.p4) > 0.7), muons[0]))
    hasMuon.refine("hasMuonRecJ", cut=(op.rng_len(muRecoilJets) > 0))
    dijets = op.combine(
        cleanedJets, N=2,
        pred=lambda j1, j2: op.deltaR(j1.p4, j2.p4) > 0.6,
        samePred=lambda j1, j2: j1.pt > j2.pt)
    plots.append(Plot.make1D(
        "nCleanediJets", op.rng_len(dijets), noSel, EqBin(50, 0., 50.),
        title="Number of cleaned dijets", xTitle="N_{jj}"))
    alljetpairs = op.combine(cleanedJets, N=2, samePred=lambda j1, j2: j1.pt > j2.pt)
    minJetDR = op.rng_min(alljetpairs, lambda pair: op.deltaR(pair[0].p4, pair[1].p4))
    plots.append(Plot.make1D("minJetDR", minJetDR, noSel, EqBin(40, 0.4, 2.)))
    hasjj = noSel.refine("hasjj", cut=(op.rng_len(alljetpairs) > 0))
    heaviestjetpair = op.rng_max_element_by(alljetpairs,
                                            fun=lambda jj: op.invariant_mass(jj[0].p4, jj[1].p4))
    # few tests of combination-as-range
    op.rng_len(heaviestjetpair)
    op.select(cleanedJets, lambda j: op.NOT(op.rng_any(heaviestjetpair, lambda hj: hj == j)))
    op.select(cleanedJets, lambda j: op.NOT(  # old way of doing the above, was a regression
        op.OR(j == heaviestjetpair[0],
              j == heaviestjetpair[1])))
    nfwjetinmpair = op.rng_count(heaviestjetpair, lambda j: op.abs(j.eta) > 2.4)
    plots.append(Plot.make1D("nfwjetinheaviestjjpair", nfwjetinmpair, hasjj, EqBin(3, 0., 3.)))
    for pt in plots:
        for p in be.getProducts(pt.name):
            p.makeProduct()
    assert all(h for p in plots for h in be.getResults(p))
