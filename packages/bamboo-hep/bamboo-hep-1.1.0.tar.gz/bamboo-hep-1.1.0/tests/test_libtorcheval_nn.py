import os.path

import pkg_resources
import pytest

from helpers import isclose_float

pytest.importorskip("torch")
pytestmark = pytest.mark.skipif(
    not pkg_resources.resource_exists("bamboo", "lib/libBambooTorch.so"),
    reason="No libBambooTorch.so")

testData = os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture(scope="module")
def libtorch_nn1():
    from bamboo.root import gbl, loadLibTorch
    loadLibTorch()
    yield gbl.bamboo.TorchEvaluator(os.path.join(testData, "nn1.pt"))


def test_libtorch_load(libtorch_nn1):
    assert libtorch_nn1


def test_libtorch_evalZero(libtorch_nn1):
    from bamboo.root import gbl
    v_in = gbl.std.vector["float"]()
    for _i in range(5):
        v_in.push_back(.7)
    v_out = libtorch_nn1.evaluate(v_in)
    assert (v_out.size() == 2) and isclose_float(sum(v_out), 1.)


def test_libtorch_evalRandom(libtorch_nn1):
    from bamboo.root import gbl
    import random
    v_in = gbl.std.vector["float"]()
    for _i in range(5):
        v_in.push_back(random.uniform(0., 1.))
    v_out = libtorch_nn1.evaluate(v_in)
    assert (v_out.size() == 2) and isclose_float(sum(v_out), 1.)
