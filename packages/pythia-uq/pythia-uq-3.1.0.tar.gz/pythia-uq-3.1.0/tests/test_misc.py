""" Test pythia.misc module. """
import pytest
import numpy as np
import pythia.misc as misc


def test_shiftCoord() -> None:
    """Test affine transformation from one interval to another."""

    # normal usecase float input
    assert misc.shiftCoord(0, [-1, 1], [0, 1]) == 0.5

    # normal usecase array input
    points = np.random.uniform(0, 1, (100))
    assert np.all(misc.shiftCoord(points, [0, 1], [1, 3]) == 2*points+1)

    # nothing happens if both intervals are the same
    assert misc.shiftCoord(0, [-1, 1], [-1, 1]) == 0

    # shifting values outside of original interval
    points = np.array([-2, 2])
    assert np.all(misc.shiftCoord(points, [0, 1], [1, 3]) == [-3, 5])


def test_cardProd() -> None:
    """Test build of cartesian product."""
    # empty list raises error
    with pytest.raises(ValueError):
        _ = misc.cartProd([]) == []

    # one array in list returns reshaped array
    array = np.arange(10)
    assert np.all(misc.cartProd([array]) == array.reshape(-1, 1))

    # only one point in each dimension
    array = [np.array([j]) for j in range(10)]
    assert np.all(misc.cartProd(array) == np.arange(10).reshape(1, -1))

    # single array is treated as n-D list with one point each
    # (same result as previous test)
    array = np.arange(10)
    assert np.all(misc.cartProd(array) == array.reshape(1, -1))

    # multiple arrays of different length (standard usecase)
    result = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]])
    assert np.all(misc.cartProd([np.arange(2), np.arange(3)]) == result)


def test_is_containted() -> None:
    """Test containment of points in domain."""

    # normal usecase 1-dim input (float or int)
    assert misc.is_contained(0.5, [0, 1]) is True  # point in domain
    assert misc.is_contained(0, [0, 1]) is True  # left boundary of domain
    assert misc.is_contained(1, [0, 1]) is True  # right boundary of domain
    assert misc.is_contained(-1, [0, 1]) is False  # point outside domain

    # normal usecase n-dim input (array, list or tuple)
    domain = [[0, 1], [0, 1], [0, 1]]
    assert misc.is_contained(0.5*np.ones(3), domain) is True  # in domain
    assert misc.is_contained([0, 0, 0], domain) is True  # boundary of domain
    assert misc.is_contained((2, 0, 0), domain) is False  # outside of domain


def test_formatTime() -> None:
    """Test correct formatting of time for printing."""

    # negative times cause assertion error
    with pytest.raises(AssertionError):
        _ = misc.formatTime(-1)

    # zero returns zero
    assert misc.formatTime(0) == "0s"

    # result is rounded to next full seconds
    assert misc.formatTime(1.2) == "2s"

    # normal usecase
    assert misc.formatTime(1234567) == "14 days 6h 56min 8s"


def test_now() -> None:
    """Test now formatting string.

    .. note::
        Testing is not necessary for a simple time formatting string.
    """
    pass


def test_line() -> None:
    """Test printing of separator line."""

    # empty indicator raises error
    with pytest.raises(AssertionError):
        _ = misc.line("")

    # normal line is 80 characters wide
    assert misc.line("-") == "-"*80

    # repeat indicator sequence until 80 characters reached
    assert misc.line("-+#") == "-+#"*26 + "-+"

    # added label doesn't change line length of 80 characters
    assert misc.line("-", "PyThia") == "-- PyThia " + "-"*70


def test_save() -> None:
    """Test save wrapper.

    .. note::
        Testing is not necessary as this is a wrapper for ``numpy.save()``.
    """
    pass


def test_load() -> None:
    """Test load wrapper.

    .. note::
        Testing is not necessary as this is a wrapper for ``numpy.load()``.
    """
    pass


def test_str2iter() -> None:
    """Test casting of str(list) to list."""

    # empty string raises error
    assert misc.str2iter("", list, int) == []
    assert misc.str2iter("", tuple, int) == ()

    # cast string representation of list to iterable
    assert misc.str2iter("[1,2,3]", list, int) == [1, 2, 3]

    # spaces are irrelevant
    assert misc.str2iter("[1, 2, 3]", list, int) == [1, 2, 3]

    # one element is cast correctly
    assert misc.str2iter("[1]", tuple, float) == (1.0,)

    # casting from tuple is ok
    assert misc.str2iter("(1, 2, 3)", list, int) == [1, 2, 3]

    # using trailing ',' is ignored
    assert misc.str2iter("(1,)", list, int) == [1]
    assert misc.str2iter("(1, )", list, int) == [1]
    assert misc.str2iter("[1, ]", list, int) == [1]


def test_batch() -> None:
    """Test batching of iterable."""

    # batchsize of zero is not allowed
    batch = misc.batch(range(10), 0)
    with pytest.raises(ValueError):
        next(batch)

    # empty iterator returns empty batch
    batch = misc.batch(range(0), 5)
    with pytest.raises(StopIteration):
        next(batch)

    # batches are generated as expected
    iterable = range(12)
    batch = misc.batch(iterable, 5)
    assert next(batch) == range(5)
    assert next(batch) == range(5, 10)
    assert next(batch) == range(10, 12)

    # batchsize larger then length of iterator returns iterator unchanged
    iterable = range(10)
    batch = misc.batch(iterable, 12)
    assert next(batch) == range(10)


def test_wlsSamplingBound() -> None:
    """Test computation of weighted Least-Squares sampling bound."""

    # m must be positive
    with pytest.raises(AssertionError):
        _ = misc.wlsSamplingBound(m=0, c=1)
    with pytest.raises(AssertionError):
        _ = misc.wlsSamplingBound(m=-10, c=1)

    # c must be positive
    with pytest.raises(AssertionError):
        _ = misc.wlsSamplingBound(m=10, c=0)
    with pytest.raises(AssertionError):
        _ = misc.wlsSamplingBound(m=10, c=-1)

    # standard usecase
    assert misc.wlsSamplingBound(m=10, c=1) == 36
    assert misc.wlsSamplingBound(m=25, c=4) == 648


def test_paramDictToList() -> None:
    """Test conversion of pt.Parameter dictionary to index-ordered list.

    .. note::
        This function is deprecated. Tests are not needed anymore.
    """
    pass


def test_gelman_rubin_condition() -> None:
    """Test computation of Gelman-Rubin criterion."""

    # uncorrelated chains yield value close to 1
    chains = np.random.normal(0, 1, (3, 10000, 1))
    assert np.linalg.norm(misc.gelman_rubin_condition(chains)-1) < 1e-3

    # chains without variation (totally correlated) yield inf
    chains = np.ones((3, 1000, 1))
    assert np.all(misc.gelman_rubin_condition(chains) == np.inf)

    # correlated chains yield value greater than 1
    chains = np.arange(3000).reshape(3, 1000, 1)
    assert np.allclose(misc.gelman_rubin_condition(chains), 4.122986296365293)


def test_get_confidence_interval() -> None:
    """Test computation of confidence intervals."""

    smpl_uni = np.random.uniform(-1, 1, (int(1e+7), 1))

    # test symmetric mass distribution
    confidence_interval = misc.get_confidence_interval(
        smpl_uni, rate=0.5, resolution=10000)
    assert np.linalg.norm(confidence_interval-np.array([[-0.5, 0.5]])) < 1e-2

    # test rate = 0 gives median
    confidence_interval = misc.get_confidence_interval(
        smpl_uni, rate=0.0, resolution=10000)
    assert np.linalg.norm(confidence_interval-np.array([[0.0, 0.0]])) < 1e-2

    # test rate = 1 gives complete domain
    confidence_interval = misc.get_confidence_interval(
        smpl_uni, rate=1.0, resolution=10000)
    assert np.linalg.norm(confidence_interval-np.array([[-1.0, 1.0]])) < 1e-2

    # test asymmetric mass distribution
    smpl_tri = np.random.triangular(0, 1, 5, (int(1e+6), 1))

    def conf_int(r):
        """Confidence interval for triangular density with a=0, b=5 and c=1."""
        assert 0 <= r <= 1
        z2 = 5-np.sqrt(10-10*r)
        z1 = np.sqrt(5/2-5*r/2) if r > 3/5 else 5 - np.sqrt(10+10*r)
        return np.array([[z1, z2]])
    for rate in [0.1, 0.6, 0.9]:  # these are relatively nice conf intervals
        interval = misc.get_confidence_interval(
            smpl_tri, rate=rate, resolution=10_000)
        assert np.linalg.norm(conf_int(rate)-interval) < 1e-2

    # test non-scalar parameter shape
    smpl_uni_multi = smpl_uni.reshape(-1, 5)
    val = np.ones((smpl_uni_multi.shape[1], 2)) * np.array([[-0.5, 0.5]])
    interval = misc.get_confidence_interval(
        smpl_uni_multi, rate=0.5, resolution=10_000)
    assert np.linalg.norm(val-interval) < 1e-2

    # test no variation in data
    smpl_one = np.ones((1, 1))
    confidence_interval = misc.get_confidence_interval(
        smpl_one, rate=0.5, resolution=10000)
    val = np.ones((smpl_one.shape[1], 2))
    assert np.linalg.norm(confidence_interval-val) < 1e-2
    confidence_interval = misc.get_confidence_interval(
        smpl_one, rate=1.0, resolution=10000)
    assert np.linalg.norm(confidence_interval-val) < 1e-2
    confidence_interval = misc.get_confidence_interval(
        smpl_one, rate=0.0, resolution=10000)
    assert np.linalg.norm(confidence_interval-val) < 1e-2


def test_doerfler_marking() -> None:
    # empty set cannot be marked
    with pytest.raises(AssertionError):
        _ = misc.doerfler_marking([], threshold=0.9)

    # test single element set
    _, _, marker = misc.doerfler_marking([1], threshold=0.9)
    assert marker == 1

    # test truncation of zeros
    test_set = np.array([0, 0, 5, 0])
    idx, values, marker = misc.doerfler_marking(test_set, threshold=0.9)
    assert np.array_equal(test_set[idx], values)
    assert np.array_equal(values[:marker], np.array([[5]]))

    # test normal use case
    test_set = np.array([0.5, 0.3, 0.1, 0.05, 0.05])
    idx, values, marker = misc.doerfler_marking(test_set, threshold=0.85)
    assert np.array_equal(values[:marker], np.array(
        [0.5, 0.3, 0.1]).reshape(-1, 1))

    # enforce marked set is larger (strict) then threshold times test set
    test_set = np.array([0.5, 0.3, 0.1, 0.05, 0.05]).reshape(-1, 1)
    idx, values, marker = misc.doerfler_marking(test_set, threshold=0.9)
    assert np.array_equal(values[:marker], np.array(
        [0.5, 0.3, 0.1, 0.05]).reshape(-1, 1))
