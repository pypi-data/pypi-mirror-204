""" Test pythia.parameter module. """
import pytest
import numpy as np
import pythia.parameter as parameter


def test_parameter() -> None:
    """Test Parameter class."""
    param1 = parameter.Parameter(0, "uni", [0, 1], "uniform")
    assert isinstance(param1, parameter.Parameter)
    assert param1.name == "uni"
    assert param1.index == 0
    assert np.all(param1.domain == np.array([0, 1]))
    assert param1.distribution == "uniform"
    assert param1.mean is None
    assert param1.var is None
    assert param1.alpha is None
    assert param1.beta is None

    param2 = parameter.Parameter(1, "nor", [-np.inf, np.inf], "normal",
                                 mean=0, var=1)
    assert param2.mean == 0.0
    assert param2.var == 1.0
    assert param2.alpha is None
    assert param2.beta is None

    param3 = parameter.Parameter(2, "beta", [-1, 1], "beta",
                                 alpha=1, beta=1)
    assert param3.mean is None
    assert param3.var is None
    assert param3.alpha == 1
    assert param3.beta == 1

    with pytest.raises(ValueError):  # bernoulli is unsupported distribution
        _ = parameter.Parameter(-1, "_", [-1, 1], "bernoulli", mean=0, var=-1)

    with pytest.raises(AssertionError):  # mean is not None
        _ = parameter.Parameter(-1, "_", [-1, 1], "uniform", mean=0)

    with pytest.raises(AssertionError):  # alpha is not None
        _ = parameter.Parameter(-1, "_", [-np.inf, np.inf], "normal",
                                mean=0, var=1, alpha=1)

    with pytest.raises(AssertionError):  # var is missing
        _ = parameter.Parameter(-1, "_", [-np.inf, np.inf], "normal", mean=0)

    with pytest.raises(AssertionError):  # var is smaller then zero
        _ = parameter.Parameter(-1, "_", [-np.inf, np.inf], "normal",
                                mean=0, var=-1)

    with pytest.raises(AssertionError):  # mean is not None
        _ = parameter.Parameter(-1, "_", [-1, 1], "beta",
                                mean=0, alpha=1, beta=1)

    with pytest.raises(AssertionError):  # alpha is missing
        _ = parameter.Parameter(-1, "_", [-1, 1], "beta", beta=1)
