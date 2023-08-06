""" Test pythia.basis module. """
from unittest.mock import MagicMock
import pytest
import numpy as np
import scipy.stats
from scipy.integrate import quad
from scipy.special import gamma, factorial, legendre, jacobi, laguerre

import pythia.basis as basis


def test_set_legendre_basis() -> None:
    """Test assembling of shifted Legendre basis functions."""
    # test if Hermite basis is orthogonal with correct scaling
    deg = 5
    param = MagicMock()
    param.domain = [-1, 2]
    base = basis.set_legendre_basis(param, deg)
    assert len(base) == deg+1
    expected = np.diag([(param.domain[1]-param.domain[0])/(2*j+1)
                       for j in range(deg+1)])
    gramian = np.zeros((deg+1, deg+1))
    for row, p in enumerate(base):
        for col, q in enumerate(base):
            def integrand(y):
                return p(y) * q(y)
            gramian[row, col] = quad(integrand, *param.domain)[0]
    assert np.linalg.norm(expected-gramian) < 1e-10


def test_set_hermite_basis() -> None:
    """Test assembling of scaled Hermite basis functions."""
    # test if missing (optional) parameter attributes are detected
    param = MagicMock()
    param.domain = [-np.inf, np.inf]
    param.mean = 1
    with pytest.raises(AssertionError):
        _ = basis.set_hermite_basis(param, 5)
    param.var = "2"
    with pytest.raises(AssertionError):
        _ = basis.set_jacobi_basis(param, 5)

    # test if Hermite basis is orthogonal with correct scaling
    deg = 5
    param = MagicMock()
    param.domain = [-np.inf, np.inf]
    param.mean = 0.5
    param.var = 1.75
    base = basis.set_hermite_basis(param, deg)
    assert len(base) == deg+1
    expected = np.diag([np.sqrt(2*np.pi) * factorial(j)
                       for j in range(deg+1)])
    gramian = np.zeros((deg+1, deg+1))
    for row, p in enumerate(base):
        for col, q in enumerate(base):
            def integrand(y):
                var = param.var
                pdf = 1 / np.sqrt(var) * np.exp(-(y-param.mean)**2 / (2*var))
                return p(y) * q(y) * pdf
            gramian[row, col] = quad(integrand, *param.domain)[0]
    assert np.linalg.norm(expected-gramian) < 1e-10


def test_set_jacobi_basis() -> None:
    """Test assembling of shifted Jacobi basis functions.

    The standard Jacobi polynomials shifted to the interval :math:`[a,b]`
    satisfy the orthogonality relation

    .. math::
        \\int_a^b P_m^{(\\beta-1,\\alpha-1)}(y) P_n^{(\\beta-1,\\alpha-1)}(y) (y-a)^{\\alpha-1} (b-y)^{\\beta-1}\\,\\mathrm{d}y
        =  \\frac{(b-a)^{\\alpha+\\beta-1}}{2m+\\alpha+\\beta-1} \\frac{1}{m!} \\frac{\\Gamma(m+\\alpha)\\Gamma(m+\\beta)}{\\Gamma(m+\\alpha+\\beta-1)} \\delta_{mn}.
    """
    # test if missing (optional) parameter attributes are detected
    param = MagicMock()
    param.domain = [-2, 7]
    param.alpha = 1
    with pytest.raises(AssertionError):
        _ = basis.set_jacobi_basis(param, 5)
    param.beta = "2"
    with pytest.raises(AssertionError):
        _ = basis.set_jacobi_basis(param, 5)

    # test if Jacobi basis is orthogonal with correct scaling
    def factor(m, alpha, beta):
        """Compute the scaling of the inner product of Jacobi polynomials."""
        width = param.domain[1] - param.domain[0]
        numerator = width**(alpha+beta-1) * gamma(m+alpha) * gamma(m+beta)
        denominator = ((2*m+alpha+beta-1) * factorial(m)
                       * gamma(m+alpha+beta-1))
        # Note: The Jacobi polynomials created by PyThia have a normalized
        #       leading coefficient. This is why the scalar product needs to be
        #       scaled accordingly by the leading coefficient of the standard
        #       Jacobi polynomials and the m-th power of the leading
        #       coefficient of the shift :math:` y \\mapsto 2/(b-a) (y-a) - 1`.
        lead_coeff = jacobi(m, beta-1, alpha-1).coeffs[0]
        normalization_scale = ((param.domain[1]-param.domain[0])**(2*m)
                               / (2**(2*m) * lead_coeff**2))
        return normalization_scale * numerator / denominator
    deg = 5
    param = MagicMock()
    param.domain = [1, 4]
    param.alpha = 1
    param.beta = 2
    base = basis.set_jacobi_basis(param, deg)
    assert len(base) == deg+1
    expected = np.diag([factor(j, param.alpha, param.beta)
                       for j in range(deg+1)])
    gramian = np.zeros((deg+1, deg+1))
    for row, p in enumerate(base):
        for col, q in enumerate(base):
            def integrand(y):
                a = param.domain[0]
                b = param.domain[1]
                pdf = (y-a)**(param.alpha-1) * (b-y)**(param.beta-1)
                return p(y) * q(y) * pdf
            gramian[row, col] = quad(integrand, *param.domain)[0]
    assert np.linalg.norm(expected-gramian) < 1e-10


def test_set_laguerre_basis() -> None:
    """Test assembling of shifted and scaled Laguerre basis functions.

    The standard Laguerre polynomials scaled with :math:`\\beta` and shifted to
    the interval :math:`(a,\\infty)` satisfy the orthogonality relation

    .. math::
        \\int_a^\\infty P_m^{\\alpha-1}(y) P_n^{\\alpha-1}(y) (y-a)^{\\alpha-1} \\exp(-\\beta(y-a))\\,\\mathrm{d}y
        = \\frac{\\Gamma(m+\\alpha)}{\\beta^{\\alpha} m!} \\delta_{mn}.
    """

    # test if missing (optional) parameter attributes are detected
    param = MagicMock()
    param.domain = [1, np.inf]
    param.alpha = 1
    with pytest.raises(AssertionError):
        _ = basis.set_laguerre_basis(param, 5)
    param.beta = "2"
    with pytest.raises(AssertionError):
        _ = basis.set_laguerre_basis(param, 5)

    # test if Laguerre basis is orthogonal with correct scaling
    def factor(m, alpha, beta):
        """Compute the scaling of the inner product of Laguerre polynomials."""
        numerator = gamma(m+alpha)
        denominator = beta**alpha * factorial(m)
        # Note: The Laguerre polynomials created by PyThia have a normalized
        #       leading coefficient. This is why the scalar product needs to be
        #       scaled accordingly by the leading coefficient of the standard
        #       Laguerre polynomials and the m-th power of the leading
        #       coefficient of the shift :math:`y \\mapsto \\beta (y-a)`.
        lead_coeff = laguerre(m, alpha-1).coeffs[0]
        normalization_scale = 1 / (beta**(2*m) * lead_coeff**2)
        return normalization_scale * numerator / denominator
    deg = 5
    param = MagicMock()
    param.domain = [1, np.inf]
    param.alpha = 1.0
    param.beta = 2.0
    base = basis.set_laguerre_basis(param, deg)
    assert len(base) == deg+1
    expected = np.diag([factor(j, param.alpha, param.beta)
                       for j in range(deg+1)])
    gramian = np.zeros((deg+1, deg+1))
    for row, p in enumerate(base):
        for col, q in enumerate(base):
            def integrand(y):
                a = param.domain[0]
                w = (y-a)**(param.alpha-1) * np.exp(-param.beta*(y-a))
                return p(y) * q(y) * w
            gramian[row, col] = quad(integrand, *param.domain)[0]
    assert np.linalg.norm(expected-gramian) < 1e-10


def test_normalize_polynomial() -> None:
    """Test normalization of polynomial bases."""
    deg = 5

    # normalization of Legendre basis
    def w_uni(y):
        return scipy.stats.uniform.pdf(
            y, loc=param.domain[0], scale=param.domain[1]-param.domain[0])
    param = MagicMock()
    param.domain = [-1, 2]
    base = basis.set_legendre_basis(param, deg)
    base = basis.normalize_polynomial(w_uni, base, param)
    gramian = np.zeros(deg+1)
    for j, poly in enumerate(base):
        def int_uni(y):
            return poly(y)**2 * w_uni(y)
        gramian[j] = quad(int_uni, *param.domain)[0]
    assert np.linalg.norm(gramian - np.ones(deg+1)) < 1e-10

    # normalization of Hermite basis
    def w_norm(y):
        return scipy.stats.norm.pdf(
            y, loc=param.mean, scale=np.sqrt(param.var))
    param = MagicMock()
    param.domain = [-np.inf, np.inf]
    param.mean = 1
    param.var = 2
    base = basis.set_hermite_basis(param, deg)
    base = basis.normalize_polynomial(w_norm, base, param)
    gramian = np.zeros(deg+1)
    for j, poly in enumerate(base):
        def int_norm(y):
            return poly(y)**2 * w_norm(y)
        gramian[j] = quad(int_norm, *param.domain)[0]
    assert np.linalg.norm(gramian - np.ones(deg+1)) < 1e-10

    # normalization of Laguerre basis
    def w_gamma(y):
        val = y - param.domain[0]
        return scipy.stats.gamma.pdf(val, a=param.alpha, scale=1/param.beta)
    param = MagicMock()
    param.domain = [1, np.inf]
    param.alpha = 1
    param.beta = 2
    base = basis.set_laguerre_basis(param, deg)
    base = basis.normalize_polynomial(w_gamma, base, param)
    gramian = np.zeros(deg+1)
    for j, poly in enumerate(base):
        def int_gamma(y):
            return poly(y)**2 * w_gamma(y)
        gramian[j] = quad(int_gamma, *param.domain)[0]
    assert np.linalg.norm(gramian - np.ones(deg+1)) < 1e-10

    # normalization of Jacobi basis
    def w_beta(y):
        a, b = param.domain
        val = (y-a) / (b-a)
        return scipy.stats.beta.pdf(val, a=param.alpha, b=param.beta)/(b-a)
    param = MagicMock()
    param.domain = [1, 5]
    param.alpha = 2
    param.beta = 0.5
    base = basis.set_jacobi_basis(param, deg)
    base = basis.normalize_polynomial(w_beta, base, param)
    gramian = np.zeros(deg+1)
    for j, poly in enumerate(base):
        def int_beta(y):
            return poly(y)**2 * w_beta(y)
        gramian[j] = quad(int_beta, *param.domain)[0]
    assert np.linalg.norm(gramian - np.ones(deg+1)) < 1e-10


def test_univariate_basis() -> None:
    """Test creation of univariate normalized polynomial basis."""

    # test correct assign of basis polynomials
    def weight(y, param):
        if param.distribution == "uniform":
            return scipy.stats.uniform.pdf(
                y, loc=param.domain[0], scale=param.domain[1]-param.domain[0])
        # return normal pdf
        return scipy.stats.norm.pdf(
            y, loc=param.mean, scale=np.sqrt(param.var))
    deg = 5
    uni_param = MagicMock()
    uni_param.domain = [0, 1]
    uni_param.distribution = "uniform"
    norm_param = MagicMock()
    norm_param.domain = [-np.inf, np.inf]
    norm_param.mean = 0
    norm_param.var = 1
    norm_param.distribution = "normal"
    params = [uni_param, norm_param]
    base = basis.univariate_basis(params, [deg]*len(params))
    for param, polys in zip(params, base):
        gramian = np.zeros(deg+1)
        for j, poly in enumerate(polys):
            def integrand(y):
                return poly(y)**2 * weight(y, param)
            gramian[j] = quad(integrand, *param.domain)[0]
        assert np.linalg.norm(gramian - np.ones(deg+1)) < 1e-10


def test_multivariate_basis() -> None:
    """Test creation of multivariate normalized polynomial basis."""

    param_basis = [[legendre(j) for j in range(3)]]*2
    mdx = np.array([[0, 0], [1, 0], [0, 1], [0, 2]])

    # test handling of shape mismatch
    with pytest.raises(AssertionError):
        _ = basis.multivariate_basis(param_basis, mdx[:, :1])
    with pytest.raises(AssertionError):
        _ = basis.multivariate_basis(param_basis, mdx, partial=[1, 0, 0])

    # test computation of basis
    base = basis.multivariate_basis(param_basis, mdx)
    for j, idx in enumerate(mdx):
        y = np.random.uniform(-1, 1, (1, 2))
        expected = (param_basis[0][idx[0]](y[0, 0])
                    * param_basis[1][idx[1]](y[0, 1]))
        assert np.linalg.norm(base[j](y) - expected) <= 1e-14

    # test computation of partial derivatives
    partial = [0, 1]
    base2 = basis.multivariate_basis(param_basis, mdx, partial)
    assert np.all(np.abs(base2[0](np.random.uniform(-1, 1, 100)) < 1e-14))
    ys = np.random.uniform(-1, 1, 200).reshape(100, 2)
    assert np.all(np.abs(base2[-1](ys) - 3*base[-2](ys)) < 1e-14)
