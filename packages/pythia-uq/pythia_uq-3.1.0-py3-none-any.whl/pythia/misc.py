"""Miscellaneous functions to support PyThia core functionality.

SPDX-License-Identifier: LGPL-3.0-or-later OR Hippocratic-3.0-ECO-MEDIA-MIL
"""
import os
import datetime
import shutil
import numpy as np
from typing import List, Tuple, Sequence, Iterator, Optional, Union, Dict


def shiftCoord(x: Union[float, np.ndarray],
               T: Union[np.ndarray, List],
               I: Union[np.ndarray, List]
               ) -> np.ndarray:
    """Shift `x` in interval `T` to interval `I`.

    Use an affine transformation to shift points :math:`x` from the interval
    :math:`T = [t_0, t_1]` to the interval :math:`I = [a, b]`.

    Parameters
    ----------
    x : array_like
        Points in interval :math:`T`.
    T : array_like
        Original interval.
    I : array_like
        Target interval.

    Returns
    -------
    :
        Shifted values for `x`.
    """
    return ((I[1]-I[0])*x + I[0]*T[1] - I[1]*T[0]) / (T[1]-T[0])


def cartProd(array_list: Union[List[np.ndarray], np.ndarray]) -> np.ndarray:
    """Compute the outer product of two or more arrays.

    Assemble an array containing all possible combinations of the elements
    of the input vectors :math:`v_1,\\dots,v_n`.

    Parameters
    ----------
    array_list : list of array_like
        List of vectors :math:`v_1,\\dots,v_n`.

    Returns
    -------
    :
        Cartesian product array.
    """
    dim = len(array_list)
    if dim == 1:
        return np.array(array_list).T
    x = np.hstack((np.meshgrid(*array_list))).swapaxes(0, 1).reshape(dim, -1).T
    return x


def is_contained(val: Union[float, Sequence, np.ndarray],
                 domain: Union[List, np.ndarray]
                 ) -> bool:
    """Check if a given value (vector) is contained in a domain.

    Checks if each component of the vector lies in the one dimensional
    interval of the corresponding component of the domain.

    Parameters
    ----------
    val : array_like
        Vector to check containment in domain
    domain : array_like
        Product domain of one dimensional intervals.

    Returns
    -------
    :
        Bool stating if value is contained in domain.
    """
    if not isinstance(val, np.ndarray):
        val = np.array(val)
    if not isinstance(domain, np.ndarray):
        domain = np.array(domain)
    if val.ndim < 2:
        val.shape = 1, -1
    if domain.ndim < 2:
        domain.shape = 1, -1
    assert val.ndim == 2
    assert val.shape[0] == 1
    assert domain.ndim == 2 and domain.shape[1] == 2
    if np.all(domain[:, 0] <= val) and np.all(val <= domain[:, 1]):
        return True
    return False


def formatTime(dt: float) -> str:
    """Converts time (seconds) to time format string.

    Parameters
    ----------
    dt : float
        Time in seconds.

    Returns
    -------
    :
        Formatted time string.
    """
    assert dt >= 0
    dct = {}
    dct['d'], rem = divmod(int(dt), 86400)
    dct['h'], rem = divmod(int(rem), 3600)
    dct['min'], seconds = divmod(int(rem), 60)
    dct['sec'] = seconds+1  # rounding seconds up
    fmt = ''
    if dct['d'] != 0:
        fmt += '{d} days '
    if dct['h'] != 0:
        fmt += '{h}h '
    if dct['min'] != 0:
        fmt += '{min}min '
    if dct['sec'] > 1:
        fmt += '{sec}s '
    if dt < 1.0:
        fmt += '{:2.2g}s'.format(dt)
    fmt = fmt.strip()
    return fmt.format(**dct)


def now() -> str:
    """Get string of current machine date and time.

    Returns
    -------
    :
        Formatted date and time string.
    """
    dt = datetime.datetime.now()
    today = '{:04}-{:02}-{:02} '.format(dt.year, dt.month, dt.day)
    now = '{:02}:{:02}:{:02}'.format(dt.hour, dt.minute, dt.second)
    return today + now


def line(indicator: str, message: str = None) -> str:
    """Print a line of 80 characters by repeating indicator.

    An additional message can be given.

    Parameters
    ----------
    indicator : string
        Indicator the line consists of, e.g. '-', '+' or '+-'.
    message : string, optional
        Message integrated in the line.

    Returns
    -------
    :
        String of 80 characters length.
    """
    assert len(indicator) > 0
    text = ''
    if message is not None:
        text = 2*indicator
        text = text[:2] + ' ' + message + ' '
    while len(text) < 80:
        text += indicator
    return text[:80]


def save(filename: str, data: np.ndarray, path: str = './') -> None:
    """Wrapper for numpy save.

    Assures path directory is created if necessary and backup old data if
    existent.

    Parameters
    ----------
    name : str
        Filename to save data to.
    data : array_like
        Data to save as .npy file.
    path : str, default='./'
        Path under which the file should be created.
    """
    if not os.path.isdir(path):
        os.makedirs(path)
    if os.path.isfile(path+filename):
        shutil.copyfile(path+filename, path+filename+'.backup')
    np.save(path+filename, data)


def load(filename: str) -> np.ndarray:
    """Alias for numpy.load()."""
    return np.load(filename)


def str2iter(string: str,
             iterType: type = list,
             dataType: type = int
             ) -> Sequence:
    """Cast `str(iterable)` to `iterType` of `dataType`.

    Cast a string of lists, tuples, etc to the specified iterable and data
    type, i.e., for `iterType=tuple` and `dataType=float` cast
    ``str([1,2,3]) -> (1.0, 2.0, 3.0)``.

    Parameters
    ----------
    string : str
        String representation of iterable.
    iterType : iterable, default=list
        Iterable type the string is converted to.
    dataType : type, default=int
        Data type of entries of iterable, e.g. `int` or `float`.
    """
    items = [s.strip() for s in string[1:-1].split(",")]
    if items[-1] == "":
        items = items[:-1]
    return iterType([dataType(item) for item in items])


def batch(iterable: Sequence, n: int = 1) -> Iterator:
    """Split iterable into different batches of batchsize n.

    Parameters
    ----------
    iterable : array_like
        Iterable to split.
    n : int, default=1
        Batch size.

    Yields
    ------
    :
        Iterable for different batches.
    """
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def wlsSamplingBound(m: int, c: float = 4) -> int:
    """Compute the weighted Least-Squares sampling bound.

    The number of samples :math:`n` is chosen such that

    .. math::
        \\frac{n}{\\log(n)} \\geq cm,

    where :math:`m` is the dimension of the Gramian matrix (number of PC
    expansion terms) and :math:`c` is an arbitrary constant. In
    Cohen & Migliorati 2017 the authors observed that the coice :math:`c=4`
    yields a well conditioned Gramian with high probability.

    Parameters
    ----------
    m : int
        Dimension of Gramian matrix.
    c : float, default=4
        Scaling constant.

    Returns
    -------
    :
        Number of required wLS samples.
    """
    assert m > 0 and c > 0
    jj = max(int(np.ceil(c*m*np.log(c*m))), 2)
    while True:
        if jj / np.log(jj) >= c*m:
            n = jj
            break
        jj += 1
    return n


def gelman_rubin_condition(chains: np.ndarray) -> np.ndarray:
    """Compute Gelman-Rubin criterion.

    Implementation of the Gelman-Rubin convergence criterion for multiple
    parameters.  A Markov chain is said to be in its convergence, if the final
    ration is close to one.

    Parameters
    ----------
    chains : array_like, ndim=3
        Array containing the Markov chains of each parameter. All chains are
        equal in length, the assumed shape is
        ``(#chains, chain length, #params)``.

    Returns
    -------
    :
        Values computed by Gelman-Rubin criterion for each parameter.
    """
    assert chains.ndim == 3
    M, N, DIM = chains.shape  # chains shape is (#chains, len(chains), #params)

    # Mean and var of chains.
    chain_means = np.mean(chains, axis=1)  # shape is (#chains, #params)
    chain_vars = np.var(chains, axis=1)  # shape is (#chains, #params)

    # Mean across all chains.
    mean = np.mean(chain_means, axis=0).reshape(1, -1)  # shape = (1, #params)

    # Between chain variance.
    B = N / (M-1) * np.sum((chain_means-mean)**2, axis=0)
    # Within chain variance.
    W = 1 / M * np.sum(chain_vars, axis=0)
    # pooled variance
    V = (N-1)/N*W + (M+1)/(M*N)*B

    return np.array([np.sqrt(v/w) if w > 0 else np.inf for v, w in zip(V, W)])


def get_confidence_interval(samples: np.ndarray,
                            rate: float = 0.95,
                            resolution: int = 500
                            ) -> np.ndarray:
    """Compute confidence intervals of samples.

    Compute the confidence intervals of the 1D marginals of the samples
    (slices).  The confidence interval of a given rate is the interval around
    the median (not mean) of the samples containing roughly `rate` percent of
    the total mass.  This is computed for the left and right side of the median
    independently.

    Parameters
    ----------
    samples : array_like, ndim < 3
        Array containing the (multidimensional) samples.
    rate : float, default=0.95
        Fraction of the total mass the interval should contain.
    resolution : int, default=500
        Number of bins used in histogramming the samples.

    Returns
    -------
    :
        Confidence intervals for each component.
    """
    if samples.ndim < 2:
        samples.shape = -1, 1
    assert samples.ndim == 2
    assert 0 <= rate <= 1
    conf_intervals = np.empty((samples.shape[1], 2))
    for j, s in enumerate(samples.T):
        median = np.median(s)
        hist, bdry = np.histogram(s, bins=resolution, density=True)
        median_bin = np.argmax(bdry > median)-1
        cumsum_left = (
            np.cumsum(np.flip(hist[:median_bin+1]))
            - 0.5*hist[median_bin]  # do not count the median bin twice
        )
        cumsum_right = (
            np.cumsum(hist[median_bin:])
            - 0.5*hist[median_bin]  # do not count the median bin twice
        )
        lc = median_bin - np.argmax(cumsum_left >= rate*cumsum_left[-1])
        rc = np.argmax(cumsum_right >= rate*cumsum_right[-1]) + median_bin
        conf_intervals[j] = np.array([bdry[lc], bdry[rc+1]])
    return conf_intervals


def doerfler_marking(values: Union[np.ndarray, List],
                     idx: Optional[np.ndarray] = None,
                     threshold: float = 0.9
                     ) -> Tuple[np.ndarray, np.ndarray, int]:
    """Dörfler marking for arbitrary values.

    Parameters
    ----------
    values : array_like
        Values for the Dörfler marking.
    idx : list of int, optional
        List of indices associated with the entries of `values`.
        If `None`, this is set to ``range(len(values))``.
    threshold : float, default=0.9
        Threshold paramter for Dörfler marking.

    Returns
    -------
    idx_reordered :
        Reordered indices given by `idx`.
        Ordered from largest to smallest value.
    ordered_values :
        Reordered values. Ordered from largest to smallest.
    marker :
        Threshold marker such that
        ``sum(values[:marker]) > threshold * sum(values)``.
    """
    if isinstance(values, list):
        values = np.array(values)
    assert values.size > 0
    if values.ndim < 2:
        values.shape = -1, 1
    assert values.ndim == 2
    if idx is None:
        idx = np.arange(values.shape[0], dtype=int)
    # index list of largest to smalles (absolute) coeff values
    sort = np.flip(np.argsort(np.abs(values), axis=None), axis=0)
    idx_reordered = idx[sort]
    ordered_values = values[sort]
    marker = int(np.argmax(
        np.cumsum(ordered_values, axis=0) > threshold*np.sum(values)))
    return idx_reordered, ordered_values, marker+1


if __name__ == '__main__':
    pass
