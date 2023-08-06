import os
import os.path

import pytest

# check if libtensorflow can be found
# (duplicates loadTensorflowC, but cannot just try to load because libtorch should be loaded first)
from bamboo.root import findLibrary
from helpers import isclose_float

tfc_found = findLibrary("libtensorflow")
if not tfc_found:
    if "VIRTUAL_ENV" in os.environ:
        tfclib_guessed_path = os.path.join(
            os.environ["VIRTUAL_ENV"], "lib", "libtensorflow.so")
        if os.path.exists(tfclib_guessed_path):
            tfc_found = tfclib_guessed_path
pytestmark = pytest.mark.skipif(not tfc_found, reason="Tensorflow-C not found")

testData = os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture(scope="module")
def tfc_nn1():
    from bamboo.root import gbl, loadTensorflowC
    loadTensorflowC()

    def vstring(*args):
        res = gbl.std.vector["std::string"]()
        for arg in args:
            res.push_back(arg)
        return res

    yield gbl.bamboo.TensorflowCEvaluator(
        os.path.join(testData, "nn1.pb"),
        vstring("dense_1_input"),
        vstring("dense_3/Softmax"))


def test_tfc_load(tfc_nn1):
    assert tfc_nn1


def test_tfc_evalZero(tfc_nn1):
    from bamboo.root import gbl
    v_in = gbl.std.vector["float"]()
    for _i in range(5):
        v_in.push_back(.7)
    v_out = tfc_nn1.evaluate(v_in)
    assert (v_out.size() == 2) and isclose_float(sum(v_out), 1.)


def test_tfc_evalRandom(tfc_nn1):
    from bamboo.root import gbl
    import random
    v_in = gbl.std.vector["float"]()
    for _i in range(5):
        v_in.push_back(random.uniform(0., 1.))
    v_out = tfc_nn1.evaluate(v_in)
    assert (v_out.size() == 2) and isclose_float(sum(v_out), 1.)
