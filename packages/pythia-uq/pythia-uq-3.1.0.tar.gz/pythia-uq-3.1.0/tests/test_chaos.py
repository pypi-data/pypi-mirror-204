"""Test pythia.chaos module."""
from unittest.mock import MagicMock
import numpy as np

from pythia import chaos


def test_PolynomialChaos() -> None:
    """Test PolynomialChaos."""

    def fun_1(x): return np.array(x[:, 0]**2 + x[:, 1]**2).reshape(-1, 1)
    def fun_2(x): return np.array(2*x[:, 0]).reshape(-1, 1)

    def mock_sobol_to_indices(sdx):
        if sdx[0] == (1,):
            return [np.array([[1, 0], [2, 0]])]
        if sdx[0] == (2,):
            return [np.array([[0, 1], [0, 2]])]
        if sdx[0] == (1, 2):
            return [np.array([[1, 1]])]
        raise NotImplementedError

    def mock_index_number(mdx):
        if np.linalg.norm(mdx[0] - np.array([0, 0])) < 1e-14:
            return np.array([0], dtype=int)
        if np.linalg.norm(mdx[0] - np.array([1, 0])) < 1e-14:
            return np.array([2, 5], dtype=int)
        if np.linalg.norm(mdx[0] - np.array([0, 1])) < 1e-14:
            return np.array([1, 3], dtype=int)
        if np.linalg.norm(mdx[0] - np.array([1, 1])) < 1e-14:
            return np.array([4], dtype=int)
        raise NotImplementedError

    param = MagicMock()
    param.domain = [-1, 1]
    param.distribution = "uniform"

    index_set = MagicMock()
    index_set.indices = np.array(
        [[0, 0], [0, 1], [1, 0], [0, 2], [1, 1], [2, 0]])
    index_set.sobol_tuples = [(1,), (2,), (1, 2)]
    index_set.max = np.array([2, 2], dtype=int)
    index_set.sobol_tuple_to_indices = MagicMock(
        side_effect=mock_sobol_to_indices)
    index_set.get_index_number = MagicMock(side_effect=mock_index_number)

    x_train = np.random.uniform(-1, 1, (100_000, 2))
    w_train = 1 / x_train.shape[0] * np.ones(x_train.shape[0])
    y_train = fun_1(x_train)

    pc = chaos.PolynomialChaos(
        [param, param], index_set, x_train, w_train, y_train)

    # test basic properties
    assert isinstance(pc, chaos.PolynomialChaos)
    assert np.linalg.cond(pc.gramian) < 1.1
    eye = np.eye(pc.gramian.shape[0])
    assert np.linalg.norm(pc.gramian-eye) < 1e-1

    # test approximation
    x_test = np.random.uniform(-1, 1, (1000, 2))
    assert np.linalg.norm(
        fun_1(x_test)-pc.eval(x_test), axis=0)[0] < 1e-10
    assert np.linalg.norm(
        fun_2(x_test)-pc.eval(x_test, partial=[1, 0]), axis=0)[0] < 1e-10

    # test mean, var and std
    assert np.linalg.norm(pc.mean-2/3) < 1e-10
    assert np.linalg.norm(pc.var-(8/45)) < 1e-10
    assert np.linalg.norm(pc.std-np.sqrt(8/45)) < 1e-10

    # test sobol indices
    assert np.linalg.norm(pc.sobol - np.array([[0.5], [0.5], [0]])) < 1e-10

    # test multi dimensional function output shape
    y_train = np.concatenate([fun_1(x_train)]*3, axis=1)
    pc = chaos.PolynomialChaos(
        [param, param], index_set, x_train, w_train, y_train)
    assert pc.coefficients.ndim == 2 and pc.coefficients.shape[1] == 3
    assert np.linalg.norm(pc.coefficients-pc.coefficients[:, :1]) < 1e-14
    assert pc.eval(x_train).shape == y_train.shape
    assert pc.sobol.shape == (3, 3)


def test_find_optimal_indices() -> None:
    """Test find_optimal_indices."""
    def fun_1(x):
        return np.array(x[:, 0]**2 + 1e-02*x[:, 1]**2).reshape(-1, 1)

    param = MagicMock()
    param.domain = [-1, 1]
    param.distribution = "uniform"

    x_train = np.random.uniform(-1, 1, (1000, 2))
    w_train = np.ones(x_train.shape[0]) / x_train.shape[0]
    y_train = fun_1(x_train)
    max_terms = 25

    indices, sobol = chaos.find_optimal_indices(
        [param, param], x_train, w_train, y_train, max_terms, threshold=1e-03)
    expected = np.array([np.arange(25), np.zeros(25)], dtype=int).T
    assert np.all(indices == expected)
    assert sobol[0, 0] > 1e-03
    assert sobol[1, 0] < 1e-03
    assert sobol[2, 0] < 1e-10

    indices, sobol = chaos.find_optimal_indices(
        [param, param], x_train, w_train, y_train,
        max_terms=10, threshold=1e-06)
    expected = np.array([[0, 0], [0, 1], [1, 0], [0, 2], [2, 0],
                         [0, 3], [3, 0], [0, 4], [4, 0]])
    assert np.all(indices == expected)
    assert sobol[0, 0] > 1e-06
    assert sobol[1, 0] > 1e-06
    assert sobol[2, 0] < 1e-10


def test_assemble_indices() -> None:
    """Test assemble_indices."""
    sobol_tuples = [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
    enum_idx = [0, 3, 2, 6]
    max_terms = 200
    val = chaos.assemble_indices(enum_idx, sobol_tuples, max_terms)
    assert val.shape[0] < max_terms
    assert val.shape[1] == 3
    assert [0, 0, 1] in val.tolist()
    assert [1, 1, 0] in val.tolist()
    assert [0, 1, 0] not in val.tolist()
    assert [1, 0, 1] not in val.tolist()


def test_get_gram_batchsize() -> None:
    """Test infering batch size for Gram matrix."""
    # Don't know how to test this.
    pass


if __name__ == "__main__":
    test_PolynomialChaos()
    test_find_optimal_indices()
