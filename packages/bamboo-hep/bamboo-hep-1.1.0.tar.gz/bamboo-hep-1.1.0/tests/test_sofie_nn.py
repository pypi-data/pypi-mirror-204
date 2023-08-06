import os.path

import pytest

from helpers import isclose_float

from bamboo.root import ROOT, _rootVersion_split

pytestmark = pytest.mark.skipif(
    not hasattr(ROOT.TMVA.Experimental, "SofieFunctor") \
    # the test file nn1.onnx uses operators that are only available in ROOT>=6.27
    or (_rootVersion_split[0] == 6 and _rootVersion_split[1] <= 26),
    reason="No SOFIE support in ROOT")

testData = os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture(scope="module")
def convertedONNXSOFIE_nn1():
    onnxModelFile = os.path.join(testData, "nn1.onnx")
    parser = ROOT.TMVA.Experimental.SOFIE.RModelParser_ONNX()
    parsedModel = parser.Parse(onnxModelFile)
    sofieModelFile = os.path.join(testData, "nn1.hxx")
    sofieWeightFile = os.path.join(testData, "nn1.dat")
    parsedModel.Generate()
    parsedModel.OutputGenerated(sofieModelFile)
    yield sofieModelFile, sofieWeightFile
    os.remove(sofieModelFile)
    os.remove(sofieWeightFile)


def test_sofieEvaluator_convert(convertedONNXSOFIE_nn1):
    headerFile, weightFile = convertedONNXSOFIE_nn1
    assert os.path.isfile(headerFile) and os.path.isfile(weightFile)


@pytest.fixture(scope="module")
def sofieEvaluator_nn1(convertedONNXSOFIE_nn1):
    headerFile, weightFile = convertedONNXSOFIE_nn1
    from bamboo.root import gbl, loadBambooSOFIE
    loadBambooSOFIE()
    gbl.gInterpreter.ProcessLine(f'#include "{headerFile}"')
    modelClass = "TMVA_SOFIE_nn1::Session"
    yield gbl.bamboo.SofieEvaluator[modelClass, "float"](0, weightFile)


def test_sofieEvaluator_load(sofieEvaluator_nn1):
    assert sofieEvaluator_nn1


def test_sofie_evalZero(sofieEvaluator_nn1):
    from bamboo.root import gbl
    v_in = gbl.std.vector["float"]()
    for _i in range(5):
        v_in.push_back(.7)
    v_out = sofieEvaluator_nn1.evaluate(0, v_in)
    assert (v_out.size() == 2) and isclose_float(sum(v_out), 1.)


def test_sofie_evalRandom(sofieEvaluator_nn1):
    from bamboo.root import gbl
    import random
    v_in = gbl.std.vector["float"]()
    for _i in range(5):
        v_in.push_back(random.uniform(0., 1.))
    v_out = sofieEvaluator_nn1.evaluate(0, v_in)
    assert (v_out.size() == 2) and isclose_float(sum(v_out), 1.)
