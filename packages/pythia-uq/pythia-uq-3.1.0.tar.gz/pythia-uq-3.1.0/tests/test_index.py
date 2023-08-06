"""Test pythia.index module."""
# from unittest.mock import MagicMock
import numpy as np
from pythia import index


def test_IndexSet() -> None:
    """Test Multiindex class."""
    indices = np.array([[0, 1], [0, 0], [1, 1], [0, 0], [2, 0]], dtype=int)
    index_set = index.IndexSet(indices)

    # test get_sobol_tuple_list()
    expected = [(1,), (2,), (1, 2)]
    val = index_set.sobol_tuples
    assert len(expected) == len(val)
    assert np.all([np.all(left == right)
                  for left, right in zip(expected, val)])

    # test get_index_number()
    val = index_set.get_index_number(np.array([[2, 0], [0, 0]]))
    expected = np.array([3, 0], dtype=int)
    assert np.all(val == expected)
    assert np.all(index_set.indices[val] == np.array([[2, 0], [0, 0]]))

    # test get_sobol_tuple_number()
    val = index_set.get_sobol_tuple_number([(1,), (1, 2)])
    assert np.all(val == [0, 2])

    # test index_to_sobol_tuple()
    val = index_set.index_to_sobol_tuple(indices)
    expected = [(2,), (), (1, 2), (), (1,)]
    assert len(val) == len(expected)
    assert np.all([np.all(left == right)
                  for left, right in zip(expected, val)])

    # test sobol_tuple_to_indices()
    val = index_set.sobol_tuple_to_indices([(1,), (1, 2)])
    expected = [np.array([[2, 0]], dtype=int), np.array([[1, 1]], dtype=int)]
    assert np.all([np.all(v == e) for v, e in zip(val, expected)])


def test_sort_index_array() -> None:
    """Test sort_index_array."""
    indices = np.array([[0, 1], [0, 0], [1, 1], [0, 0], [2, 0]], dtype=int)
    expected = np.array([[0, 0], [0, 1], [1, 1], [2, 0]], dtype=int)
    assert np.all(index.sort_index_array(indices) == expected)


def test_add_indices() -> None:
    """Test add_indices."""
    indices_1 = np.array([[0, 0], [1, 0], [2, 0]], dtype=int)
    indices_2 = np.array([[0, 0], [0, 1], [0, 2]], dtype=int)
    expected = np.array([[0, 0], [0, 1], [1, 0], [0, 2], [2, 0]], dtype=int)
    assert np.all(index.add_indices([indices_1, indices_2]) == expected)


def test_subtract_indices() -> None:
    """Test subtract_indices."""
    indices = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=int)
    subtract = np.array([[1, 0], [2, 0]], dtype=int)
    expected = np.array([[0, 0], [0, 1], [1, 1]], dtype=int)
    val = index.subtract_indices(indices, subtract)
    assert np.all(val == expected)


def test_tensor() -> None:
    """Test tensor."""
    lower = [0, 1]
    shape = [3, 3]
    expected = np.array(
        [[0, 1], [0, 2], [1, 1], [1, 2], [2, 1], [2, 2]], dtype=int)
    assert np.all(index.tensor(shape, lower) == expected)

    shape = [1, 4, 2]
    lower = [0, 0, 1]
    expected = np.array(
        [[0, 0, 1], [0, 1, 1], [0, 2, 1], [0, 3, 1]], dtype=int)
    assert np.all(index.tensor(shape, lower) == expected)


def test_simplex() -> None:
    """Test simplex."""
    val = index.simplex(2, 2)
    expected = np.array(
        [[0, 0], [0, 1], [1, 0], [0, 2], [1, 1], [2, 0]], dtype=int)
    assert np.all(val == expected)

    val = index.simplex(3, 1)
    expected = np.array(
        [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]], dtype=int)
    assert np.all(val == expected)


if __name__ == "__main__":
    test_subtract_indices()
