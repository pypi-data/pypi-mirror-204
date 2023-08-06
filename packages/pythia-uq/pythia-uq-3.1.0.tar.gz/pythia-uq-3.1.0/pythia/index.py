"""Create, manipulate and store information about multiindices.

SPDX-License-Identifier: LGPL-3.0-or-later OR Hippocratic-3.0-ECO-MEDIA-MIL
"""
from typing import List, Tuple, Union, Optional
import itertools
import numpy as np
import pythia as pt


class IndexSet:
    """Generate index set object for sparse PC expansion.

    Parameters
    ----------
    indices : np.ndarray
        Array of multiindices with shape (#indices, param dim).
    """

    def __init__(self, indices: np.ndarray) -> None:
        """Initialize sparse multiindex object."""
        assert indices.ndim == 2 and indices.shape[0] > 0
        assert indices.dtype == int
        assert np.all(indices >= 0)
        self.indices = sort_index_array(indices)
        self.shape = self.indices.shape
        self.max = np.array(np.max(self.indices, axis=0), dtype=int)
        self.min = np.array(np.min(self.indices, axis=0), dtype=int)
        self.sobol_tuples = self._get_sobol_tuple_list()

    def _get_sobol_tuple_list(self) -> List:
        """Generate list of all possible Sobol index id tuples (subscripts).

        Returns
        -------
        :
            List of Sobol tuples.
        """
        sobol_tuples = []
        for r in range(1, self.shape[1]+1):
            sobol_tuples += list(
                itertools.combinations(range(1, self.shape[1]+1), r))
        return sobol_tuples

    def get_index_number(self, indices: np.ndarray) -> np.ndarray:
        """Get enumeration number of indices.

        Get the row indices of the given multiindices such that
        `self.indices[rows] = indices`.

        Parameters
        ----------
        indices : np.ndarray
            Indices to get the number of.

        Returns
        -------
        :
            Array containing the enumeration numbers of the indices.
        """
        return np.array([np.where((self.indices == index).all(axis=1))[0]
                         for index in indices], dtype=int).flatten()

    def get_sobol_tuple_number(self, sobol_tuples: List[tuple]) -> np.ndarray:
        """Get enumeration indices of Sobol tuples.

        Parameters
        ----------
        sobol_tuples : list of tuple
            List of Sobol tuples.

        Returns
        -------
        :
            Array containing the enumeration number of the Sobol tuples.
        """
        return np.array([self.sobol_tuples.index(s) for s in sobol_tuples],
                        dtype=int)

    def index_to_sobol_tuple(self, indices: np.ndarray) -> List[Tuple]:
        """Map array of indices to their respective Sobol tuples.

        Parameters
        ----------
        indices : np.ndarray
            Array of multiindices.

        Returns
        -------
        :
            List of Sobol tuples.
        """
        sobol_tuples = [tuple(np.flatnonzero(index)+1) for index in indices]
        return sobol_tuples

    def sobol_tuple_to_indices(self,
                               sobol_tuples: Union[tuple, List[tuple]]
                               ) -> List[np.ndarray]:
        """Map Sobol tuples to their respective indices.

        Parameters
        ----------
        sobol_tuples : tuple or list of tuple
            List of Sobol tuples.

        Returns
        -------
        :
            List of index arrays for each given Sobol tuple.
        """
        if isinstance(sobol_tuples, tuple):
            sobol_tuples = [sobol_tuples]
        assert isinstance(sobol_tuples, list)
        ret = []
        lookup_dict = {sobol_tuple: [] for sobol_tuple in self.sobol_tuples}
        index_sobol_tuple_list = self.index_to_sobol_tuple(self.indices)
        for sobol_tuple, index in zip(index_sobol_tuple_list, self.indices):
            if len(sobol_tuple) > 0:
                lookup_dict[sobol_tuple] += [index]
        for sobol_tuple in sobol_tuples:
            ret += [np.array(lookup_dict[sobol_tuple], dtype=int)]
        return ret


def sort_index_array(indices: np.ndarray) -> np.ndarray:
    """Sort multiindices and remove duplicates.

    Sort rows of `indices` by sum of multiindex and remove duplicate
    multiindices.

    Parameters
    ----------
    indices : np.ndarray
        Index list before sorting.

    Returns
    -------
    :
        Sorted index array.
    """
    sorted_indices = np.unique(indices, axis=0)
    idx = np.argsort(np.sum(sorted_indices, axis=1))
    sorted_indices = sorted_indices[idx]
    return np.array(sorted_indices, dtype=int)


def add_indices(index_list: List[np.ndarray]) -> np.ndarray:
    """Add multiple arrays of multiindices.

    Concatenate multiple arrays of multiindices, remove duplicates and sort
    them by sum of multiindices.

    Parameters
    ----------
    index_list : list of np.ndarray
        List of multiindex arrays.

    Returns
    -------
    :
        Array with all multiindices.
    """
    all_indices = np.concatenate(index_list, axis=0)
    return sort_index_array(all_indices)


def subtract_indices(indices: np.ndarray, subtract: np.ndarray) -> np.ndarray:
    """Set difference of two index arrays.

    Parameters
    ----------
    indices : np.ndarray
        Index array multiindices are taken out of.
    subtract : np.ndarray
        Indices that are taken out of the original set.

    Returns
    -------
    :
        Set difference of both index arrays.
    """
    indices = sort_index_array(indices)
    subtract = sort_index_array(subtract)
    assert indices.shape[1] == subtract.shape[1]
    idxs = []
    for mdx in subtract:
        idx = np.where((indices == mdx).all(axis=1))[0]
        assert idx.size < 2
        if idx.size == 1:
            idxs += [idx]
    return np.delete(indices, np.array(idxs, dtype=int).flatten(), axis=0)


def tensor(shape: Union[List, Tuple, np.ndarray],
           lower: Optional[Union[List, Tuple, np.ndarray]] = None
           ) -> np.ndarray:
    """Create a tensor index set.

    Parameters
    ----------
    shape : array_like
        Shape of the tensor, enumeration starting from 0.
    lower : array_like, default = None
        Starting values for each dimension of the tensor set. If None, all
        dimensions start with 0.

    Returns
    -------
    :
        Array with all possible multiindices in tensor set.

    Examples
    --------
    >>> pt.index.tensor([2, 2])
    array([[0, 0],
           [0, 1],
           [1, 0],
           [1, 1]])

    It is also possible to use the tensor functions to create n-variate subsets
    for the overall tensor set.

    >>> pt.index.tensor([1, 5, 2], [0, 2, 0])
    array([[0, 2, 0],
           [0, 2, 1],
           [0, 3, 0],
           [0, 3, 1],
           [0, 4, 0],
           [0, 4, 1]])
    """
    shape = np.array(shape, dtype=int)
    if lower is None:
        lower = np.zeros(shape.size, dtype=int)
    elif isinstance(lower, (list, tuple)):
        lower = np.array(lower, dtype=int)
    assert shape.size == lower.size
    univariate_dims = [np.arange(low, up, dtype=int)
                       for low, up in zip(lower, shape)]
    if shape.size > 1:
        ret = pt.misc.cartProd(univariate_dims)
    else:
        ret = np.array(univariate_dims).T
    return sort_index_array(ret)


def simplex(dimension: int, maximum: int) -> np.ndarray:
    """Create a simplex index set.

    A simplex index set consists of all multiindices with sum less then or
    equal the maximum given.

    Parameters
    ----------
    dimension : int
        Dimension of the multiindices.
    maximum : int
        Maximal sum value for the multiindices.

    Returns
    -------
    :
        Array with all possible multiindices in simplex set.

    Examples
    --------
    >>> pt.index.simplex(2, 2)
    array([[0, 0],
           [0, 1],
           [1, 0],
           [0, 2],
           [1, 1],
           [2, 0]])
    """
    assert dimension > 0 and maximum > 0
    all_indices = tensor([maximum+1]*dimension)
    rows = np.where(np.sum(all_indices, axis=1) <= maximum)[0]
    return sort_index_array(all_indices[rows])
