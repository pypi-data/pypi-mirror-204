""" Test pythia.basis module. """
from unittest.mock import MagicMock
import numpy as np
from scipy.special import gamma
from scipy.integrate import quad

import pythia.sampler as sampler


def test_UniformSampler() -> None:
    """Test uniform sampler."""

    domain = [-1, 2]
    diam = domain[1] - domain[0]
    s = sampler.UniformSampler(domain)

    # test general properties
    assert isinstance(s, sampler.Sampler)
    assert isinstance(s.domain, np.ndarray)
    assert s.dimension == 1
    assert s.mass == 1
    assert np.abs(s.maximum - 1 / diam) < 1e-12
    assert np.abs(s.mean - 0.5) < 1e-12
    assert np.abs(s.var - 3/4) < 1e-12
    assert np.abs(s.std - np.sqrt(3)/2) < 1e-12

    # test pdf
    vals = s.pdf(np.random.uniform(*domain, 100))
    assert vals.shape == (100,)
    assert np.all(vals - 1/diam) < 1e-12

    # test log-pdf
    vals = s.log_pdf(np.random.uniform(*domain, 100))
    assert vals.shape == (100,)
    assert np.all(vals - np.log(1/diam)) < 1e-12

    # test grad log-pdf
    vals = s.grad_x_log_pdf(np.random.uniform(*domain, 100))
    assert vals.shape == (100,)
    assert np.all(vals) < 1e-12

    # test hessian log-pdf
    vals = s.hess_x_log_pdf(np.random.uniform(*domain, 100))
    assert vals.shape == (100,)
    assert np.all(vals) < 1e-12

    # test sampling
    # Note: There is no reasonable way to reliably test if moments of
    #       distribution are correct (without drawing a lot of samples)
    samples = s.sample((100, 1))
    assert samples.shape == (100, 1)
    assert np.all(samples > domain[0]) and np.all(samples < domain[1])


def test_NormalSampler() -> None:
    """Test normal sampler."""

    mean = 1
    var = 4
    s = sampler.NormalSampler(mean, var)

    # test general properties
    assert isinstance(s, sampler.Sampler)
    assert isinstance(s.domain, np.ndarray)
    assert np.abs(s.mean - 1) < 1e-12
    assert np.abs(s.var - 4) < 1e-12
    assert np.abs(s.std - 2) < 1e-12
    assert s.dimension == 1
    assert s.mass == 1
    assert np.abs(s.maximum - 1 / np.sqrt(2*np.pi*var)) < 1e-12

    # test pdf
    xs = np.random.normal(mean, np.sqrt(var), 100)
    vals = s.pdf(xs)
    expected = np.exp(-0.5 * (xs-mean)**2 / var) / np.sqrt(2*np.pi*var)
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test log-pdf
    xs = np.random.normal(mean, np.sqrt(var), 100)
    vals = s.log_pdf(xs)
    expected = -0.5 * (xs-mean)**2 / var - np.log(np.sqrt(2*np.pi*var))
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test grad log-pdf
    xs = np.random.normal(mean, np.sqrt(var), 100)
    vals = s.grad_x_log_pdf(xs)
    expected = - (xs-mean) / var
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test hessian log-pdf
    xs = np.random.normal(mean, np.sqrt(var), 100)
    vals = s.hess_x_log_pdf(xs)
    expected = - 1 / var
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test sampling
    # Note: There is no reasonable way to reliably test if moments of
    #       distribution are correct (without drawing a lot of samples)
    assert s.sample((100, 1)).shape == (100, 1)


def test_GammaSampler() -> None:
    """Test gamma sampler."""

    domain = [1, np.inf]
    alpha = 1
    beta = 3
    s = sampler.GammaSampler(domain, alpha, beta)

    # test general properties
    assert isinstance(s, sampler.Sampler)
    assert isinstance(s.domain, np.ndarray)
    assert s.dimension == 1
    assert s.mass == 1
    assert s.alpha == 1
    assert s.beta == 3
    assert np.abs(s.mean - 4/3) < 1e-12
    assert np.abs(s.var - 1/9) < 1e-12
    assert np.abs(s.std - 1/3) < 1e-12
    assert np.abs(s.maximum - 3) < 1e-12

    # test pdf
    xs = np.random.gamma(alpha, 1/beta, 100) + domain[0]
    vals = s.pdf(xs)
    expected = 3 * np.exp(-3*(xs-domain[0]))  # pdf for alpha=1 and beta=3
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test log-pdf
    xs = np.random.gamma(alpha, 1/beta, 100) + domain[0]
    vals = s.log_pdf(xs)
    expected = np.log(3) - 3*(xs-domain[0])  # log-pdf for alpha=1 and beta=3
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test grad log-pdf
    # Note: not yet implemented.

    # test hessian log-pdf
    # Note: not yet implemented.

    # test sampling
    # Note: There is no reasonable way to reliably test if moments of
    #       distribution are correct (without drawing a lot of samples)
    assert s.sample((100, 1)).shape == (100, 1)


def test_BetaSampler() -> None:
    """Test beta sampler."""

    domain = [1, 5]
    length = domain[1]-domain[0]
    alpha = 2
    beta = 2
    s = sampler.BetaSampler(domain, alpha, beta)

    # test general properties
    assert isinstance(s, sampler.Sampler)
    assert isinstance(s.domain, np.ndarray)
    assert s.dimension == 1
    assert s.mass == 1
    assert s.alpha == 2
    assert s.beta == 2
    assert np.abs(s.mean - 3) < 1e-12
    assert np.abs(s.var - 1/5) < 1e-12
    assert np.abs(s.std - 1/np.sqrt(5)) < 1e-12
    assert np.abs(s.maximum - 6/16) < 1e-12

    # test pdf
    Beta = gamma(4) / (gamma(2)*gamma(2))
    xs = np.random.beta(alpha, beta, 100)*length + domain[0]
    vals = s.pdf(xs)
    # pdf for alpha=2 and beta=2
    expected = length**(-3) * Beta * (xs-domain[0]) * (domain[1] - xs)
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test log-pdf
    xs = np.random.beta(alpha, beta, 100)*length + domain[0]
    vals = s.log_pdf(xs)
    expected = (-3*np.log(length) + np.log(Beta)
                + np.log(xs-domain[0]) + np.log(domain[1]-xs))
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test grad log-pdf
    # Note: not yet implemented.

    # test hessian log-pdf
    # Note: not yet implemented.

    # test sampling
    # Note: There is no reasonable way to reliably test if moments of
    #       distribution are correct (without drawing a lot of samples)
    assert s.sample((100, 1)).shape == (100, 1)


def test_WLSUnivariateSampler() -> None:
    """Test univariate wls sampler.

    .. note::
        This currently only tests uniform WLS sampling.
    """

    param = MagicMock()
    param.distribution = "uniform"
    param.domain = [-1, 1]
    s = sampler.WLSUnivariateSampler(param, deg=5, tsa=True)
    # define normalized Legendre basis polynomials
    basis = [np.polynomial.legendre.Legendre([0]*j+[1], param.domain)
             for j in range(6)]
    scales = [quad(lambda x: 0.5*p(x)**2, param.domain[0], param.domain[1])[0]
              for p in basis]
    basis = [p / np.sqrt(scale) for (p, scale) in zip(basis, scales)]

    # test general properties
    assert isinstance(s, sampler.Sampler)
    assert isinstance(s.domain, np.ndarray)
    assert s.dimension == 1
    assert s.mass == 1
    assert np.abs(s.mean - 0.0) < 1e-10
    assert np.abs(s.var - 0.4965034965034964) < 1e-10
    assert np.abs(s.std - np.sqrt(0.4965034965034964)) < 1e-10
    assert np.abs(s.maximum - 3) < 1e-10

    # test weight
    xs = np.random.uniform(param.domain[0], param.domain[1], 100)
    expected = 6 / np.sum([np.abs(p(xs))**2 for p in basis], axis=0)
    vals = s.weight(xs)
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test pdf
    xs = np.random.uniform(param.domain[0], param.domain[1], 100)
    vals = s.pdf(xs)
    expected = 1/12 * np.sum([np.abs(p(xs))**2 for p in basis], axis=0)
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test log-pdf
    xs = np.random.uniform(param.domain[0], param.domain[1], 100)
    vals = s.log_pdf(xs)
    expected = np.log(np.sum([np.abs(p(xs))**2 for p in basis], axis=0)/12)
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test grad log-pdf
    # Note: not yet implemented.

    # test hessian log-pdf
    # Note: not yet implemented.

    # test _compute_trial_sampler
    xs = np.random.uniform(param.domain[0], param.domain[1], 100)
    trial_sampler, bulk = s._compute_trial_sampler()
    assert np.all(bulk*trial_sampler.pdf(xs) > s.pdf(xs))

    # test sampling
    # Note: There is no reasonable way to reliably test if moments of
    #       distribution are correct (without drawing a lot of samples)
    assert s.sample((100, 1)).shape == (100, 1)


def test_ProductSampler() -> None:
    """Test product sampler."""

    # NOTE: Mock samplers do not resemble real univariate samplers.
    sampler_1 = MagicMock()
    sampler_1.domain = np.array([[-1, 3]])
    sampler_1.maximum = 1/4
    sampler_1.mean = 1.0
    sampler_1.cov = 4/3
    sampler_1.pdf = lambda x: 1/4*np.ones(x.shape[0])
    sampler_1.log_pdf = lambda x: np.log(1/4)*np.ones(x.size)
    sampler_1.grad_x_log_pdf = lambda x: 1/4*np.ones(x.size)
    sampler_1.hess_x_log_pdf = lambda x: 1/4*np.ones(x.size)
    sampler_1.sample = lambda shape: np.ones(shape)

    sampler_2 = MagicMock()
    sampler_2.domain = np.array([[-np.inf, np.inf]])
    sampler_2.maximum = 1 / np.sqrt(4*np.pi)
    sampler_2.mean = 2.0
    sampler_2.cov = 2.0
    sampler_2.pdf = lambda x: np.exp(-x**2/2)
    sampler_2.log_pdf = lambda x: -x**2/2
    sampler_2.grad_x_log_pdf = lambda x: -x
    sampler_2.hess_x_log_pdf = lambda x: -x
    sampler_2.sample = lambda shape: np.ones(shape)

    s = sampler.ProductSampler([sampler_1, sampler_2])

    # test general properties
    assert isinstance(s, sampler.Sampler)
    assert isinstance(s.domain, np.ndarray)
    assert np.linalg.norm(s.domain[0] - np.array([-1, 3])) < 1e-12
    assert np.all(np.isinf(s.domain[1]))
    assert s.dimension == 2
    assert s.mass == 1
    assert np.abs(s.maximum - 1 / (8*np.sqrt(np.pi))) < 1e-12
    assert np.linalg.norm(s.mean - [1, 2]) < 1e-12
    assert np.linalg.norm(s.cov - np.diag([4/3, 2])) < 1e-12

    # test pdf
    xs = np.random.uniform(-1, 3, (100, 2))
    expected = 1/4 * np.exp(-xs[:, 1]**2/2)
    assert s.pdf(xs).shape == (100,)
    assert np.max(np.abs(s.pdf(xs) - expected)) < 1e-12

    # test log-pdf
    xs = np.random.uniform(-1, 3, (100, 2))
    expected = np.log(1/4) - xs[:, 1]**2/2
    assert s.log_pdf(xs).shape == (100,)
    assert np.max(np.abs(s.log_pdf(xs) - expected)) < 1e-12

    # test grad log-pdf
    xs = np.random.uniform(-1, 3, (100, 2))
    expected = np.array([1/4*np.ones(xs.shape[0]), - xs[:, 1]]).T
    assert s.grad_x_log_pdf(xs).shape == (100, 2)
    assert np.max(np.abs(s.grad_x_log_pdf(xs) - expected)) < 1e-12

    # test hessian log-pdf
    xs = np.random.uniform(-1, 3, (100, 2))
    expected = np.zeros((100, 2, 2))
    expected[:, 0, 0] = 1/4*np.ones(xs.shape[0])
    expected[:, 1, 1] = - xs[:, 1]
    assert s.hess_x_log_pdf(xs).shape == (100, 2, 2)
    assert np.max(np.abs(s.hess_x_log_pdf(xs) - expected)) < 1e-12

    # test sampling
    # Note: There is no reasonable way to reliably test if moments of
    #       distribution are correct (without drawing a lot of samples)
    assert np.linalg.norm(s.sample((100, 1)) - np.ones((100, 1, 2))) < 1e-12


def test_ParameterSampler() -> None:
    """Test parameter sampler."""
    param1 = MagicMock()
    param1.distribution = "normal"
    param1.domain = [-np.inf, np.inf]
    param1.mean = 0.0
    param1.var = 1.0

    param2 = MagicMock()
    param2.distribution = "normal"
    param2.domain = [-np.inf, np.inf]
    param2.mean = 1.0
    param2.var = 2.0

    s = sampler.ParameterSampler([param1, param2])

    # test general properties
    assert isinstance(s, sampler.Sampler)
    assert isinstance(s.domain, np.ndarray)
    assert np.all(s.domain.shape == (2, 2))
    assert np.all(np.isinf(s.domain))
    assert s.dimension == 2
    assert s.mass == 1
    assert np.abs(s.maximum - 1 / (np.sqrt(2)*2*np.pi)) < 1e-12
    assert np.linalg.norm(s.mean - [0, 1]) < 1e-12
    assert np.linalg.norm(s.cov - np.diag([1, 2])) < 1e-12

    # test pdf
    xs = np.random.multivariate_normal(s.mean, s.cov, 100)
    expected = (1/(np.sqrt(2)*2*np.pi)
                * np.exp(-xs[:, 0]**2/2 - (xs[:, 1]-1)**2/4))
    assert s.pdf(xs).shape == (100,)
    assert np.max(np.abs(s.pdf(xs) - expected)) < 1e-12

    # test log-pdf
    xs = np.random.multivariate_normal(s.mean, s.cov, 100)
    expected = (-np.log((np.sqrt(2)*2*np.pi))
                - xs[:, 0]**2/2 - (xs[:, 1]-1)**2/4)
    assert s.log_pdf(xs).shape == (100,)
    assert np.max(np.abs(s.log_pdf(xs) - expected)) < 1e-12

    # test grad log-pdf
    xs = np.random.multivariate_normal(s.mean, s.cov, 100)
    expected = np.array([-xs[:, 0], -(xs[:, 1]-1)/2]).T
    assert s.grad_x_log_pdf(xs).shape == (100, 2)
    assert np.max(np.abs(s.grad_x_log_pdf(xs) - expected)) < 1e-12

    # test hessian log-pdf
    xs = np.random.multivariate_normal(s.mean, s.cov, 100)
    expected = np.zeros((100, 2, 2))
    expected[:, 0, 0] = -np.ones(xs.shape[0])
    expected[:, 1, 1] = -np.ones(xs.shape[0])/2.0
    assert s.hess_x_log_pdf(xs).shape == (100, 2, 2)
    assert np.max(np.abs(s.hess_x_log_pdf(xs) - expected)) < 1e-12

    # test sampling
    # Note: There is no reasonable way to reliably test if moments of
    #       distribution are correct (without drawing a lot of samples)
    assert s.sample((100, 1)).shape == (100, 1, 2)


def test_WLSSampler() -> None:
    """Test weighted least-squares sampler."""
    param = MagicMock()
    param.distribution = "uniform"
    param.domain = [-1, 1]

    # define normalized Legendre basis polynomials
    basis = [np.polynomial.legendre.Legendre([0]*j+[1], param.domain)
             for j in range(6)]
    scales = [quad(lambda x: 0.5*p(x)**2, param.domain[0], param.domain[1])[0]
              for p in basis]
    basis = [p / np.sqrt(scale) for (p, scale) in zip(basis, scales)]
    m_basis = []
    for p in basis:
        for q in basis:
            def func(x, p=p, q=q):
                return p(x[:, 0])*q(x[:, 1])
            m_basis.append(func)
    s = sampler.WLSSampler([param, param], m_basis, tsa=True)

    # test general properties
    assert isinstance(s, sampler.Sampler)
    assert isinstance(s.domain, np.ndarray)
    assert s.dimension == 2
    assert s.mass == 1
    assert np.abs(s.maximum - 9) < 1e-10

    # Note: mean and cov not implemented

    # test weight
    xs = np.random.uniform(param.domain[0], param.domain[1], (100, 2))
    expected = (6**2 / np.prod(np.sum(
        [np.abs(p(xs))**2 for p in basis], axis=0), axis=1))
    vals = s.weight(xs)
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test pdf
    xs = np.random.uniform(param.domain[0], param.domain[1], (100, 2))
    vals = s.pdf(xs)
    expected = 1/12**2 * np.prod(np.sum(
        [np.abs(p(xs))**2 for p in basis], axis=0), axis=1)
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test log-pdf
    xs = np.random.uniform(param.domain[0], param.domain[1], (100, 2))
    vals = s.log_pdf(xs)
    expected = np.sum(np.log(np.sum(
        [np.abs(p(xs))**2 for p in basis], axis=0)), axis=1) - np.log(12**2)
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test grad log-pdf
    # Note: not yet implemented.

    # test hessian log-pdf
    # Note: not yet implemented.

    # test sampling
    # Note: There is no reasonable way to reliably test if moments of
    #       distribution are correct (without drawing a lot of samples)
    assert s.sample((100, 1)).shape == (100, 1, 2)


def test_WLSTensorSampler() -> None:
    """Test weighted least-squares tensor product sampler."""
    param = MagicMock()
    param.distribution = "uniform"
    param.domain = [-1, 1]
    s = sampler.WLSTensorSampler([param, param], [5, 5], tsa=True)

    # define normalized Legendre basis polynomials
    basis = [np.polynomial.legendre.Legendre([0]*j+[1], param.domain)
             for j in range(6)]
    scales = [quad(lambda x: 0.5*p(x)**2, param.domain[0], param.domain[1])[0]
              for p in basis]
    basis = [p / np.sqrt(scale) for (p, scale) in zip(basis, scales)]

    # test general properties
    assert isinstance(s, sampler.Sampler)
    assert isinstance(s.domain, np.ndarray)
    assert s.dimension == 2
    assert s.mass == 1
    assert np.abs(s.maximum - 9) < 1e-10
    assert np.linalg.norm(s.mean - [0, 0]) < 1e-12
    var = 0.4965034965034964
    assert np.linalg.norm(s.cov - np.diag([var, var])) < 1e-12

    # test weight
    xs = np.random.uniform(param.domain[0], param.domain[1], (100, 2))
    expected = (6**2 / np.prod(np.sum(
        [np.abs(p(xs))**2 for p in basis], axis=0), axis=1))
    vals = s.weight(xs)
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test pdf
    xs = np.random.uniform(param.domain[0], param.domain[1], (100, 2))
    vals = s.pdf(xs)
    expected = 1/12**2 * np.prod(np.sum(
        [np.abs(p(xs))**2 for p in basis], axis=0), axis=1)
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test log-pdf
    xs = np.random.uniform(param.domain[0], param.domain[1], (100, 2))
    vals = s.log_pdf(xs)
    expected = np.sum(np.log(np.sum(
        [np.abs(p(xs))**2 for p in basis], axis=0)), axis=1) - np.log(12**2)
    assert vals.shape == (100,)
    assert np.max(np.abs(vals - expected)) < 1e-12

    # test grad log-pdf
    # Note: not yet implemented.

    # test hessian log-pdf
    # Note: not yet implemented.

    # test sampling
    # Note: There is no reasonable way to reliably test if moments of
    #       distribution are correct (without drawing a lot of samples)
    assert s.sample((100, 1)).shape == (100, 1, 2)


def test_rejection_sampling() -> None:
    """Test rejection sampling."""
    # TODO(Nando): Is there a reasonable way to test rejection sampling?
    ts = MagicMock()
    ts.pdf = lambda x: np.ones(x.shape[0])
    ts.sample = lambda n: np.random.uniform(0, 1, (n, 2))
    samples = sampler.rejection_sampling(
        ts.pdf, ts, scale=1.1, dimension=2, shape=(1000, 3))
    assert samples.shape == (1000, 3, 2)


def test_constraint_sampling() -> None:
    """Test constraint sampling."""
    s = MagicMock()
    s.sample = lambda n: np.random.uniform(0, 1, (np.prod(n), 2))
    s.dimension = 2

    def constraint(x):
        if x.ndim != 1:
            x = x.reshape(-1)
        if x[0] + x[1] <= 1:
            return True
        return False

    # test sampling shape and constraint
    samples = sampler.constraint_sampling(s, [constraint], 1000)
    assert samples.shape == (1000, 2)
    assert np.all(np.sum(samples, axis=1) <= 1)


def test_assign_sampler() -> None:
    """Test assigning of correct sampler function."""
    param = MagicMock()
    param.distribution = "uniform"
    param.domain = [0, 1]
    assert isinstance(sampler.assign_sampler(param), sampler.UniformSampler)

    param = MagicMock()
    param.distribution = "normal"
    param.mean = 1
    param.var = 1
    assert isinstance(sampler.assign_sampler(param), sampler.NormalSampler)

    param = MagicMock()
    param.distribution = "gamma"
    param.domain = [1, np.inf]
    param.alpha = 2
    param.beta = 0.5
    assert isinstance(sampler.assign_sampler(param), sampler.GammaSampler)

    param = MagicMock()
    param.distribution = "beta"
    param.domain = [0, 1]
    param.alpha = 2
    param.beta = 0.5
    assert isinstance(sampler.assign_sampler(param), sampler.BetaSampler)


def test_get_maximum() -> None:
    """Test estimate of function maximum."""
    # maximum at border of domain
    val = sampler.get_maximum(
        lambda x: x[:, 0]**2 * x[:, 1]**2, [[-1, 1], [-1, 1]])
    assert np.linalg.norm(val - 1) < 1e-2

    # maximum in domain
    mean = np.random.uniform(-0.5, 0.5, (1, 2))
    val = sampler.get_maximum(
        lambda x: np.exp(- np.linalg.norm(x-mean, axis=1)**2/2),
        [[-1, 1], [-1, 1]])
    assert np.linalg.norm(val-1) < 1e-2


if __name__ == "__main__":
    pass
