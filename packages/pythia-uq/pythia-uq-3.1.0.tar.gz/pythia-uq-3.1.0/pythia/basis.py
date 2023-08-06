""" Assemble sparse univariate and multivariate basis polynomials.

Build univariate or multivariate normalized basis polynomials depending on
the domain and distribution (and other degrees of freedom) of the parameter(s).

Currently supported are the following distribution types:
    - uniform
    - normal
    - Gamma
    - Beta

SPDX-License-Identifier: LGPL-3.0-or-later OR Hippocratic-3.0-ECO-MEDIA-MIL
"""
from typing import List, Tuple, Optional, Callable, Union
import numpy as np
import scipy.integrate
import scipy.special
import pythia as pt


def univariate_basis(params: List[pt.parameter.Parameter],
                     degs: Union[List[int], Tuple[int], np.ndarray],
                     ) -> List[List[Callable]]:
    """Assemble a univariate polynomial basis.

    Set polynomial basis up to deg for each parameter in `params` according to
    the parameter distribution and area of definition.

    Parameters
    ----------
    params : list of `pythia.parameter.Parameter`
        Parameters to compute univariate basis function for.
    degs : array_like
        Max. degrees of univariate polynomials for each parameter.

    Returns
    -------
    :
        List of normalized univariate polynomials w.r.t. parameter domain and
        distribution up to specified degree for each parameter in `params`.
    """
    basis = []
    param_pdfs = [pt.sampler.assign_sampler(param).pdf for param in params]
    for param, pdf, deg in zip(params, param_pdfs, degs):
        # Set the polynomial basis with corresponding area of support and
        # proper normalization.
        if param.distribution == "uniform":
            polynomials = normalize_polynomial(
                pdf, set_legendre_basis(param, deg), param)
        elif param.distribution == "normal":
            polynomials = normalize_polynomial(
                pdf, set_hermite_basis(param, deg), param)
        elif param.distribution == "gamma":
            polynomials = normalize_polynomial(
                pdf, set_laguerre_basis(param, deg), param)
        elif param.distribution == "beta":
            polynomials = normalize_polynomial(
                pdf, set_jacobi_basis(param, deg), param)
        else:
            raise ValueError(f'Unsupported distribution "{param.distribution}"'
                             f' for {param.name}')
        basis += [polynomials]
    return basis


def multivariate_basis(univariate_bases: List[List[Callable]],
                       indices: np.ndarray,
                       partial: Optional[List[int]] = None,
                       ) -> List[Callable]:
    """Assemble multivariate polynomial basis.

    Set the (partial derivative of the) multivariate (product) polynomial basis
    functions.

    Parameters
    ----------
    univariate_bases : list of list of callable
        Univariate basis functions for parameters. Is called by
        `univariate_bases[paramIdx][deg]()`.
    indices : array_like
        Array of multiindices for multivariate basis functions.
    partial : list of int
        Number of partial derivatives for each dimension. Length is same as
        `univariate_bases`.

    Returns
    -------
    :
        List of multivariate product polynomials with univariate degrees as
        specified in `indices`.
    """
    assert len(univariate_bases) == indices.shape[1]
    if partial is not None:
        assert len(partial) == indices.shape[1]
    basis_list = []
    for index in indices:
        def fun(x: np.ndarray,
                index: Optional[np.ndarray] = index
                ) -> np.ndarray:
            if not 1 <= x.ndim <= 2:
                raise ValueError(f"Wrong ndim '{x.ndim}'")
            if x.ndim == 1:
                x.shape = 1, -1
            if partial is None:
                basis = [univariate_bases[k][mu_k]
                         for k, mu_k in enumerate(index)]
            else:
                basis = [univariate_bases[k][mu_k].deriv(partial[k])
                         for k, mu_k in enumerate(index)]
            return np.prod([basis[k](x[:, k])
                            for k, _ in enumerate(index)], axis=0)
        basis_list += [fun]
    return basis_list


def normalize_polynomial(weight: Callable,
                         basis: List[Callable],
                         param: pt.parameter.Parameter,
                         ) -> List[Callable]:
    """Normalize orthogonal polynomials.

    Normalize a polynomial of an orthogonal system with respect to the scalar
    product

    .. math::
        a(u,v)_\\mathrm{pdf} = \\int u(p) v(p) \\mathrm{pdf}(p) \\mathrm{d}p.

    The normalized polynomial :math:`\\phi_j` for any given polynomial
    :math:`P_j` is given by :math:`\\phi_j = P_j / \\sqrt{c_j}`
    for the constant
    :math:`c_j = \\int \\mathrm{pdf}(p) * P_j(p)^2 \\mathrm{d}p`.

    Parameters
    ----------
    weight : callable
        Probability density function.
    basis : list of `numpy.polynomial.Polynomial`
        Polynomials to normalize w.r.t. weight.
    param : `pythia.parameter.Parameter`
        Parameter used for distribution and domain information.

    Returns
    -------
    :
        List of normalized univariate polynomials.
    """
    cs = np.zeros(len(basis))
    for j, p in enumerate(basis):
        if param.distribution == "normal":
            cs[j] = float(np.math.factorial(j))
        else:
            def integrand(x):
                return weight(x)*p(x)**2
            cs[j], _ = scipy.integrate.quad(
                integrand, param.domain[0], param.domain[1])
    return [p/np.sqrt(c) for c, p in zip(cs, basis)]


def set_legendre_basis(param: pt.parameter.Parameter,
                       deg: int
                       ) -> List[Callable]:
    """Generate list of the Legendre Polynomials.

    Generate the Legendre Polynomials up to certain degree on the interval
    specified by the parameter.

    Parameters
    ----------
    param : `pythia.parameters.Parameter`
        Parameter for basis function. Needs to be uniformly distributed.
    deg : int
        Maximum degree for polynomials.

    Returns
    -------
    :
        List of Legendre polynomials up to (including) degree specified in
        `deg`.
    """
    return [np.polynomial.legendre.Legendre([0]*j+[1], param.domain)
            for j in range(deg+1)]


def set_hermite_basis(param: pt.parameter.Parameter,
                      deg: int
                      ) -> List[Callable]:
    """Generate list of probabilists Hermite polynomials.

    Generate the Hermite Polynomials up to certain degree according to the
    mean and variance of the specified parameter.

    Parameters
    ----------
    param : `pythia.parameters.Parameter`
        Parameter for basis function. Needs to be normal distributed.
    deg : int
        Maximum degree for polynomials.

    Returns
    -------
    :
        List of probabilists Hermite polynomials up to (including) degree
        specified in `deg`.
    """
    assert isinstance(param.mean, (int, float))
    assert isinstance(param.var, (int, float))
    p_list = []
    std = np.sqrt(param.var)
    a = -param.mean / (std * np.sqrt(2))
    b = 1 / (np.sqrt(2) * std)
    shift = np.polynomial.polynomial.Polynomial([a, b])
    for j in range(deg+1):
        p = np.polynomial.hermite.Hermite([0]*j+[1])
        p_list.append(2**(-j/2)*p(shift))
    return p_list


def set_jacobi_basis(param: pt.parameter.Parameter,
                     deg: int
                     ) -> List[Callable]:
    """Generate list of Jacobi polynomials.

    Generate the Jacobi Polynomials up to certain degree on the interval
    and DoFs specified by the parameter.

    .. note::
        The Jacobi polynomials have leading coefficient 1.

    Parameters
    ----------
    param : `pythia.parameters.Parameter`
        Parameter for basis function. Needs to be Beta-distributed.
    deg : int
        Maximum degree for polynomials.

    Returns
    -------
    :
        List of Jacobi polynomials up to (including) degree specified in `deg`.
    """
    assert isinstance(param.alpha, (int, float))
    assert isinstance(param.beta, (int, float))
    p_list = [np.polynomial.polynomial.Polynomial(1)]

    a = pt.misc.shiftCoord(0.0, [-1, 1], param.domain)
    b = pt.misc.shiftCoord(1.0, [-1, 1], param.domain) - a
    shift = np.polynomial.polynomial.Polynomial([a, b])

    for j in range(1, deg+1):
        roots, _ = scipy.special.roots_jacobi(j, param.beta-1, param.alpha-1)
        coeff = np.polynomial.polynomial.polyfromroots(shift(roots))
        p = np.polynomial.polynomial.Polynomial(coeff)
        p_list.append(p)
    return p_list


def set_laguerre_basis(param: pt.parameter.Parameter,
                       deg: int
                       ) -> List[Callable]:
    """Generate list of Leguerre polynomials.

    Generate the generalized Laguerre polynomials up to certain degree on
    the interval and DoFs specified by the parameter.

    Parameters
    ----------
    param : `pythia.parameters.Parameter`
        Parameter for basis function. Needs to be Gamma-distributed.
    deg : int
        Maximum degree for polynomials.

    Returns
    -------
    :
        List of Laguerre polynomials up to (including) degree specified in
        `deg`.
    """
    assert isinstance(param.alpha, (int, float))
    assert isinstance(param.beta, (int, float))
    p_list = [np.polynomial.polynomial.Polynomial(1)]
    shift = np.polynomial.polynomial.Polynomial(
        [param.domain[0], 1/param.beta])
    for j in range(1, deg+1):
        roots, _ = scipy.special.roots_genlaguerre(j, param.alpha-1)
        coeff = np.polynomial.polynomial.polyfromroots(shift(roots))
        p = np.polynomial.polynomial.Polynomial(coeff)
        p_list.append(p)
    return p_list


if __name__ == "__main__":
    pass
