"""Sampler classes for generating in random samples and PDF evaluations.

SPDX-License-Identifier: LGPL-3.0-or-later OR Hippocratic-3.0-ECO-MEDIA-MIL
"""
from typing import List, Tuple, Union, Callable, Optional
from abc import ABC, abstractmethod, abstractproperty
import warnings
import numpy as np
import scipy.stats
from scipy.integrate import quad
from scipy.special import gamma
import pythia as pt


class Sampler(ABC):
    """Base class for all continuous samplers. """

    # set abstract attributes
    domain: np.ndarray

    @abstractproperty
    def dimension(self) -> int:
        """Dimension of the ambient space."""
        raise NotImplementedError

    @abstractproperty
    def mass(self):
        """Mass of the sampler distribution.

        The integral of the sampler distribution over the domain of
        definition. If the density is normalised this value should be one.
        """
        raise NotImplementedError

    @abstractproperty
    def maximum(self) -> float:
        """Maximum of the pdf."""
        raise NotImplementedError

    @abstractproperty
    def mean(self) -> Union[float, np.ndarray]:
        """Mean value of the pdf."""
        raise NotImplementedError

    @abstractproperty
    def cov(self) -> Union[float, np.ndarray]:
        """(Co)Variance of the pdf."""
        raise NotImplementedError

    @abstractmethod
    def pdf(self, x: np.ndarray) -> np.ndarray:
        """Density of the samplers distribution.

        Computes the density of the samplers underlying distribution at the
        given points `x`.

        Parameters
        ----------
        x : array_like of shape (..., D)
            List of points or single point. `D` is the objects dimension.

        Returns
        -------
        :
            Density values at the points.
        """
        raise NotImplementedError

    @abstractmethod
    def log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Log-density of the samplers distribution.

        Computes the log-density of the samplers underlying distribution at the
        given points `x`.

        Parameters
        ----------
        x : array_like of shape (..., D)
            List of points or single point. `D` is the objects dimension.

        Returns
        -------
        :
            Log-density values at the points.
        """
        raise NotImplementedError

    @abstractmethod
    def grad_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Gradient of log-density of the samplers distribution.

        Computes the gradient of the log-density of the samplers underlying
        distribution at the given points `x`.

        Parameters
        ----------
        x : array_like of shape (..., D)
            List of points or single point. `D` is the objects dimension.

        Returns
        -------
        :
            Gradient values of the log-density at the points with shape
            (..., D).
        """
        raise NotImplementedError

    @abstractmethod
    def hess_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Hessian of log-density of the samplers distribution.

        Computes the Hessian of the log-density of the samplers underlying
        distribution at the given points `x`.

        Parameters
        ----------
        x : array_like of shape (..., D)
            List of points or single point. `D` is the objects dimension.

        Returns
        -------
        :
            Hessian values of the log-density at the points with shape
            (..., D, D).
        """
        raise NotImplementedError

    @abstractmethod
    def sample(self, shape: Union[List, Tuple, np.ndarray]) -> np.ndarray:
        """Random values in a given shape.

        Create an array of the given shape and populate it with random samples
        from the samplers distribution.

        Parameters
        ----------
        shape : array_like, optional
            The dimensions of the returned array, should all be positive.
            If no argument is given a single Python float is returned.

        Returns
        -------
        :
            Random values of specified shape.
        """
        raise NotImplementedError


class UniformSampler(Sampler):
    """Sampler for univariate uniformly distributed samples on given domain.

    Parameters
    ----------
    domain : array_like
        Interval of support of distribution.
    """

    def __init__(self, domain: Union[List, Tuple, np.ndarray]) -> None:
        """Initiate UniformSampler object."""
        self.domain = np.reshape(np.array(domain), (-1, 2))
        assert self.domain.shape == (1, 2)
        self._length = self.domain[0, 1] - self.domain[0, 0]

    @property
    def dimension(self) -> int:
        """Parameter dimension."""
        return self.domain.shape[0]

    @property
    def mass(self) -> float:
        """Mass of the PDF."""
        return 1

    @property
    def maximum(self) -> float:
        """Maximum value of the PDF."""
        return 1 / self._length

    @property
    def mean(self) -> float:
        """Mean value of the distribution."""
        return 0.5 * (self.domain[0, 0] + self.domain[0, 1])

    @property
    def cov(self) -> float:
        """(Co)Variance of the distribution."""
        return 1 / 12 * (self.domain[0, 1] - self.domain[0, 0])**2

    @property
    def var(self) -> float:
        """Variance of the distribution."""
        return self.cov

    @property
    def std(self) -> float:
        """Standard deviation of the distribution."""
        return np.sqrt(self.var)

    def pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate uniform PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of PDF evaluated in `x`.
        """
        return scipy.stats.uniform.pdf(
            x, loc=self.domain[0, 0], scale=self._length)

    def log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate uniform log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of log-PDF evaluated in `x`.
        """
        return scipy.stats.uniform.logpdf(
            x, loc=self.domain[0, 0], scale=self._length)

    def grad_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """ Evaluate gradient of uniform log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of gradient (vector valued) of log-PDF evaluated in `x`.
        """
        return np.zeros_like(x)

    def hess_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """ Evaluate Hessian of uniform log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of Hessian (matrix valued) of log-PDF evaluated in `x`.
        """
        return np.zeros_like(x)

    def sample(self, shape: Union[int, List, Tuple, np.ndarray]) -> np.ndarray:
        """ Draw samples from uniform distribution.

        Parameters
        ----------
        shape : array_like
            Shape of the samples.

        Returns
        -------
        :
            Random samples of specified shape.
        """
        return np.random.uniform(self.domain[0, 0], self.domain[0, 1], shape)


class NormalSampler(Sampler):
    """Sampler for univariate normally distributed samples.

    Parameters
    ----------
    mean : float
        Mean of the Gaussian distribution.
    var : float
        Variance of the Gaussian distribution.
    """

    def __init__(self, mean: float, var: float) -> None:
        """Initiate NormalSampler object."""
        self.domain = np.array([-np.inf, np.inf], ndmin=2)  # shape is (1,2)
        self._mean = mean  # work-around to comply with ABC Sampler class
        assert var >= 0
        self.var = var

    @property
    def mass(self) -> float:
        """Mass of the PDF."""
        return 1

    @property
    def dimension(self) -> float:
        """Dimension of the parameters."""
        return self.domain.shape[0]

    @property
    def maximum(self) -> float:
        """Maximum value of the PDF."""
        return 1 / np.sqrt(2*np.pi*self.var)

    @property
    def mean(self) -> float:
        """Mean value of the distribution."""
        return self._mean

    @property
    def cov(self) -> float:
        """(Co)Variance of the distribution."""
        return self.var

    @property
    def std(self) -> float:
        """Standard deviation."""
        return np.sqrt(self.var)

    def pdf(self, x: np.ndarray) -> np.ndarray:
        """ Evaluate PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of PDF evaluated in `x`.
        """
        return scipy.stats.norm.pdf(
            x, loc=self.mean, scale=np.sqrt(self.var))

    def log_pdf(self, x: np.ndarray) -> np.ndarray:
        """ Evaluate log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of log-PDF evaluated in `x`.
        """
        return scipy.stats.norm.logpdf(
            x, loc=self.mean, scale=np.sqrt(self.var))

    def grad_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """ Evaluate gradient of log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of gradient (vector valued) of log-PDF evaluated in `x`.
        """
        return - (x - self.mean) / self.var

    def hess_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """ Evaluate Hessian of log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of Hessian (matrix valued) of log-PDF evaluated in `x`.
        """
        return - 1 / self.var * np.ones_like(x)

    def sample(self, shape: Union[int, List, Tuple, np.ndarray]) -> np.ndarray:
        """ Draw samples from distribution.

        Parameters
        ----------
        shape : array_like
            Shape of the samples.

        Returns
        -------
        :
            Random samples of specified shape.
        """
        return np.random.normal(self.mean, np.sqrt(self.var), shape)


class GammaSampler(Sampler):
    """Sampler for univariate Gamma distributed samples on given domain.

    Parameters
    ----------
    domain : array_like
        Supported domain of distribution.
    alpha : float
        Parameter for Gamma distribution.
    beta : float
        Parameter for Gamma distribution.
    """

    def __init__(self,
                 domain: Union[List, Tuple, np.ndarray],
                 alpha: float,
                 beta: float
                 ) -> None:
        """Initiate GammaSampler object."""
        self.domain = np.reshape(np.array(domain), (-1, 2))
        assert self.domain.shape == (1, 2)
        assert self.domain[0, 1] == np.inf
        self.alpha = alpha
        self.beta = beta
        assert self.alpha > 0 and self.beta > 0

    @property
    def dimension(self) -> float:
        """Dimension of the parameters."""
        return 1

    @property
    def mass(self) -> float:
        """Mass of the PDF."""
        return 1

    @property
    def maximum(self) -> float:
        """Maximum value of the PDF.

        The maximum of the Gamma distribution is given by

        .. math::
            \\max_{x\\in[a,\\infty)} f(x) =
            \\begin{cases}
            \\infty & \\mbox{if } 0 < \\alpha < 1\\\\
            \\frac{\\beta^\\alpha}{\\Gamma(\\alpha)} & \\mbox{if } \\alpha = 1\\\\
            \\frac{\\beta^\\alpha}{\\Gamma(\\alpha)} \\Bigl(\\frac{\\alpha-1}{\\beta} \\Bigr)^{\\alpha-1} e^{1-\\alpha} & \\mbox{if } \\alpha > 1\\\\
            \\end{cases}
        """
        if self.alpha < 1:
            return np.inf

        if self.alpha == 1:
            return self.beta**self.alpha / gamma(self.alpha)

        return (self.beta**self.alpha / gamma(self.alpha)
                * ((self.alpha-1)/self.beta)**(self.alpha-1)
                * np.exp(-(self.alpha-1)))

    @property
    def mean(self) -> float:
        """Mean value of the distribution."""
        return self.alpha / self.beta + self.domain[0, 0]

    @property
    def cov(self) -> float:
        """(Co)Variance of the distribution."""
        return self.alpha / self.beta**2

    @property
    def var(self) -> float:
        """Variance of the distribution."""
        return self.cov

    @property
    def std(self) -> float:
        """Standard deviation of the distribution."""
        return np.sqrt(self.var)

    def pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of PDF evaluated in `x`.
        """
        y = x - self.domain[0, 0]
        return scipy.stats.gamma.pdf(y, a=self.alpha, scale=1.0/self.beta)

    def log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of log-PDF evaluated in `x`.
        """
        y = x - self.domain[0, 0]
        return scipy.stats.gamma.logpdf(y, a=self.alpha, scale=1.0/self.beta)

    def grad_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate gradient of log-PDF.

        .. note::
            Not yet implemented.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of gradient (vector valued) of log-PDF evaluated in `x`.
        """
        raise NotImplementedError

    def hess_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate Hessian of log-PDF.

        .. note::
            Not yet implemented.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of Hessian (matrix valued) of log-PDF evaluated in `x`.
        """
        raise NotImplementedError

    def sample(self, shape: Union[int, List, Tuple, np.ndarray]) -> np.ndarray:
        """Draw samples from distribution.

        Parameters
        ----------
        shape : array_like
            Shape of the samples.

        Returns
        -------
        :
            Random samples of specified shape.
        """
        ret = np.random.gamma(self.alpha, 1.0/self.beta, shape)
        return ret + self.domain[0, 0]


class BetaSampler(Sampler):
    """Sampler for univariate Beta distributed samples on given domain.

    Parameters
    ----------
    domain : array_like
        Supported domain of distribution.
    alpha : float
        Parameter for Beta distribution.
    beta : float
        Parameter for Beta distribution.
    """

    def __init__(self,
                 domain: Union[List, Tuple, np.ndarray],
                 alpha: float,
                 beta: float
                 ) -> None:
        """Initiate BetaSampler object."""
        self.domain = np.reshape(np.array(domain), (-1, 2))
        assert self.domain.shape == (1, 2)
        self.length = self.domain[0, 1] - self.domain[0, 0]
        self.alpha = alpha
        self.beta = beta
        assert self.alpha > 0 and self.beta > 0

    @property
    def dimension(self):
        """Dimension of the parameters."""
        return 1

    @property
    def mass(self):
        """Mass of the PDF."""
        return 1

    @property
    def maximum(self):
        """Maximum value of the PDF.

        The maximum of the Beta distribution is given by

        .. math::
            \\max_{x\\in[a,b]} f(x) =
            \\begin{cases}
            \\infty & \\mbox{if } 0 < \\alpha < 1 \\mbox{ or } 0 < \\beta < 1,\\\\
            \\frac{1}{(b-a)B(\\alpha,\\beta)} & \\mbox{if } \\alpha = 1 \\mbox{ or } \\beta = 1,\\\\
            \\frac{(\\alpha-1)^{\\alpha-1}(\\beta-1)^{\\beta-1}}{(\\alpha+\\beta-2)^{\\alpha+\\beta-2}(b-a)B(\\alpha,\\beta)} & \\mbox{if } \\alpha > 1 \\mbox{ and } \\beta > 1, \\\\
            \\end{cases}

        where :math:`B(\\alpha,\\beta)` denotes the Beta-function.
        """
        if self.alpha < 1 or self.beta < 1:
            return np.inf

        Beta = gamma(self.alpha)*gamma(self.beta)/gamma(self.alpha+self.beta)
        if self.alpha == 1 or self.beta == 1:
            return 1 / (Beta * self.length)

        val = ((self.alpha-1)**(self.alpha-1)
               * (self.beta-1)**(self.beta-1)
               / (self.alpha+self.beta-2)**(self.alpha+self.beta-2))
        return val / (Beta * self.length)

    @property
    def mean(self) -> float:
        """Mean value of the distribution."""
        shift = self.domain[0, 0]
        scale = self.length
        return scale * self.alpha / (self.alpha + self.beta) + shift

    @property
    def cov(self) -> float:
        """(Co)Variance of the distribution."""
        a = self.alpha
        b = self.beta
        return a*b / ((a+b)**2 * (a+b+1)) * self.length

    @property
    def var(self) -> float:
        """Variance of the distribution."""
        return self.cov

    @property
    def std(self) -> float:
        """Standard deviation of the distribution."""
        return np.sqrt(self.var)

    def pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of PDF evaluated in `x`.
        """
        y = pt.misc.shiftCoord(x, self.domain.flatten(), [0, 1])
        ret = scipy.stats.beta.pdf(y, a=self.alpha, b=self.beta)
        return ret / self.length

    def log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of log-PDF evaluated in `x`.
        """
        y = pt.misc.shiftCoord(x, self.domain.flatten(), [0, 1])
        ret = scipy.stats.beta.logpdf(y, a=self.alpha, b=self.beta)
        return ret - np.log(self.length)

    def grad_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate gradient of log-PDF.

        .. note::
            Not yet implemented.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of gradient (vector valued) of log-PDF evaluated in `x`.
        """
        raise NotImplementedError

    def hess_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate Hessian of log-PDF.

        .. note::
            Not yet implemented.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of Hessian (matrix valued) of log-PDF evaluated in `x`.
        """
        raise NotImplementedError

    def sample(self, shape: Union[int, List, Tuple, np.ndarray]) -> np.ndarray:
        """Draw samples from distribution.

        Parameters
        ----------
        shape : array_like
            Shape of the samples.

        Returns
        -------
        :
            Random samples of specified shape.
        """
        SAMPLE = np.random.beta(self.alpha, self.beta, shape)
        return pt.misc.shiftCoord(SAMPLE, [0, 1], self.domain.flatten())


class WLSUnivariateSampler(Sampler):
    """Sampler for univariate optimally distributed samples on given domain.

    Parameters
    ----------
    domain : array_like
        Interval of support of distribution.
    """

    def __init__(self,
                 param: pt.parameter.Parameter,
                 deg: int,
                 tsa: bool = True
                 ) -> None:
        """Initiate WLSUnivariateSampler object."""
        self.parameter = param
        self.deg = deg
        self._base_sampler = assign_sampler(param)
        self.domain = self._base_sampler.domain
        self._basis = pt.basis.univariate_basis(
            [self.parameter], [self.deg])[0]
        self._tsa = tsa
        self._trial_sampler, self._bulk = self._compute_trial_sampler()
        assert self.domain.shape == (1, 2)
        # self._length = self.domain[0, 1] - self.domain[0, 0]

    @property
    def dimension(self) -> int:
        """Parameter dimension."""
        return self.domain.shape[0]

    @property
    def mass(self) -> float:
        """Mass of the PDF."""
        return 1

    @property
    def maximum(self) -> float:
        """Maximum value of the PDF."""
        if self.parameter.distribution == "uniform":
            # alternatively return pdf in domain[0, 1]
            return self.pdf(self.domain[0, 0])
        elif self.parameter.distribution == "normal":
            if self.deg % 2 == 0:
                return self.pdf(self.parameter.mean)
            else:
                # Note: this can be improved
                return get_maximum(self.pdf, self.domain)
        elif self.parameter.distribution == "gamma":
            # Note: this is probably not going to work for domain = [a, inf]
            return get_maximum(self.pdf, self.domain)
        elif self.parameter.distribution == "beta":
            # Note: this can be improved
            return get_maximum(self.pdf, self.domain)
        return get_maximum(self.pdf, self.domain)

    @property
    def mean(self) -> float:
        """Mean value of the distribution."""
        mean, err = quad(
            lambda x: x*self.pdf(x), self.domain[0, 0], self.domain[0, 1])
        if err > 1e-8:
            warnings.warn(f"quadrature error large: ({err})")
        return mean

    @property
    def cov(self) -> float:
        """(Co)Variance of the distribution."""
        moment, err = quad(
            lambda x: x**2*self.pdf(x), self.domain[0, 0], self.domain[0, 1])
        if err > 1e-8:
            warnings.warn(f"quadrature error large: ({err})")
        return moment - self.mean**2

    @property
    def var(self) -> float:
        """Variance of the distribution."""
        return self.cov

    @property
    def std(self) -> float:
        """Standard deviation of the distribution."""
        return np.sqrt(self.var)

    def weight(self, x: Union[np.ndarray, float, int]) -> np.ndarray:
        """Weights for the pdf.

        Parameters
        ----------
        x : np.ndarray
            Points the weight function is evaluated in.

        Returns
        -------
        w : array_like
            Weights of evaluation points `x`.
        """
        if isinstance(x, (float, int)):
            x = np.array(x).reshape(1)
        if x.ndim == 2 and x.shape[1] == 1:
            x = np.array(x).reshape(-1)
        assert x.ndim < 2
        b_eval = np.sum([np.abs(p(x))**2 for p in self._basis], axis=0)
        return (self.deg + 1) / b_eval

    def pdf(self, x: Union[np.ndarray, float, int]) -> np.ndarray:
        """Evaluate uniform PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of PDF evaluated in `x`.
        """
        if isinstance(x, (float, int)):
            x = np.array(x).reshape(1)
        if x.ndim == 2 and x.shape[1] == 1:
            x = np.array(x).reshape(-1)
        return self._base_sampler.pdf(x) / self.weight(x)

    def log_pdf(self, x: Union[np.ndarray, float, int]) -> np.ndarray:
        """Evaluate uniform log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of log-PDF evaluated in `x`.
        """
        if isinstance(x, (float, int)):
            x = np.array(x).reshape(1)
        if x.ndim == 2 and x.shape[1] == 1:
            x = np.array(x).reshape(-1)
        return self._base_sampler.log_pdf(x) - np.log(self.weight(x))

    def grad_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """ Evaluate gradient of uniform log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of gradient (vector valued) of log-PDF evaluated in `x`.
        """
        raise NotImplementedError

    def hess_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate Hessian of uniform log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of Hessian (matrix valued) of log-PDF evaluated in `x`.
        """
        raise NotImplementedError

    def _compute_trial_sampler(self) -> Tuple[Sampler, float]:
        """Trial sampler adaptation.

        .. note::
            TSA currently only available for uniform parameter distribution.

        Parameters
        ----------
        tsa : bool
            Adapt trial sampler or simply use uniform product sampler.

        Returns
        -------
        trial_sampler : pt.sampler.Sampler
            Trial sampler.
        bulk : array_like
            Domain estimate of the mass of the distribution.
        """
        if (self._tsa is True and
                self.parameter.distribution == "uniform"):
            trial_sampler = BetaSampler(self.parameter.domain, 0.5, 0.5)
        else:
            trial_sampler = UniformSampler(self.parameter.domain)
        bulk = get_maximum(
            lambda x: self.pdf(x)/trial_sampler.pdf(x), self.domain
        )
        return trial_sampler, bulk

    def sample(self, shape: Union[int, List, Tuple, np.ndarray]) -> np.ndarray:
        """Draw samples from weighted least-squares parameter distribution.

        Parameters
        ----------
        shape : array_like
            Shape of the samples.

        Returns
        -------
        :
            Random samples of specified shape.
        """
        if isinstance(shape, int):
            shape = (shape,)
        samples = rejection_sampling(
            self.pdf, self._trial_sampler, self._bulk, self.dimension, shape)
        return samples


class ProductSampler(Sampler):
    """Tensor sampler for independent parameters.

    Sampler for cartesian product samples of a list of (independent) univariate
    samplers.

    Parameters
    ----------
    sampler_list : list of `pythia.sampler.Sampler`
        List of (univariate) Sampler objects.
    """

    def __init__(self, sampler_list: List[Sampler]) -> None:
        """ Initiate ProductSampler object. """
        self.samplers = list(sampler_list)
        self.domain = np.squeeze(np.array([s.domain for s in self.samplers]))
        # Add dimension if len(sampler_list) == 1.
        if self.domain.ndim < 2:
            self.domain.shape = 1, 2
        # sampler_list should contain 1D samplers only
        assert self.domain.shape == (len(sampler_list), 2)

    @ property
    def dimension(self) -> int:
        """Dimension of the parameters."""
        return self.domain.shape[0]

    @ property
    def mass(self) -> float:
        """Mass of the PDF."""
        return np.prod(np.array([s.mass for s in self.samplers]))

    @ property
    def maximum(self) -> float:
        """Maximum value of the PDF."""
        return np.prod(np.array([s.maximum for s in self.samplers]))

    @ property
    def mean(self) -> np.ndarray:
        """Mean of the PDF."""
        return np.array([s.mean for s in self.samplers])

    @ property
    def cov(self) -> np.ndarray:
        """Covariance of the PDF."""
        return np.diag([s.cov for s in self.samplers])

    def weight(self, x: np.ndarray) -> np.ndarray:
        """Weights of the product PDF.

        Parameters
        ----------
        x : np.ndarray
            Evaluation points.

        Returns
        -------
        :
            Array of uniform weights for samples.
        """
        if x.ndim == 1:
            x.shape = 1, -1
        assert x.ndim == 2
        return np.ones(x.shape[0])

    def pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate PDF.

        The PDF is given by the product of the univariate PDFs.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of PDF evaluated in `x`.
        """
        assert x.shape[-1] == self.dimension
        densities = [s.pdf for s in self.samplers]
        val = np.array(
            [densities[jj](x[..., jj]) for jj in range(self.dimension)])
        return np.prod(val, axis=0)

    def log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate log-PDF.

        The log-PDF is given by the sum of the univariate log-PDFs.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of log-PDF evaluated in `x`.
        """
        assert x.shape[-1] == self.dimension
        densities = [s.log_pdf for s in self.samplers]
        val = np.array(
            [densities[jj](x[..., jj]) for jj in range(self.dimension)])
        return np.sum(val, axis=0)

    def grad_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate gradient of log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of gradient (vector valued) of log-PDF evaluated in `x`.
        """
        grad_densities = [s.grad_x_log_pdf for s in self.samplers]
        return np.array([grad_densities[jj](x[..., jj])
                         for jj in range(self.dimension)]).T

    def hess_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate Hessian of log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of Hessian (matrix valued) of log-PDF evaluated in `x`.
        """
        # create an (x.shape[0], self._dim, self._dim) tensor where each
        # (self._dim, self._dim) matrix is the identity
        eye = np.tile(np.expand_dims(np.eye(self.dimension), 0),
                      (x.shape[0], 1, 1))

        # create an (x.shape[0],self._dim,1) tensor where each (x.shape[0],1,1)
        # subtensor is a diagonal entry of the hessian
        hess_densities = [s.hess_x_log_pdf for s in self.samplers]
        hess = np.expand_dims(np.array([hess_densities[jj](x[..., jj])
                                        for jj in range(self.dimension)]).T, 2)
        return eye*hess

    def sample(self, shape: Union[int, List, Tuple, np.ndarray]) -> np.ndarray:
        """Draw samples from distribution.

        Parameters
        ----------
        shape : array_like
            Shape of the samples.

        Returns
        -------
        :
            Random samples of specified shape.
        """
        if isinstance(shape, int):
            shape = (shape,)
        samples = [s.sample(shape) for s in self.samplers]
        return np.stack(samples, -1)


class ParameterSampler(Sampler):
    """Product sampler of given parameters.

    Parameters
    ----------
    params : list of `pythia.parameter.Parameter`
        List containing information of parameters.
    """

    def __init__(self, params: List[pt.parameter.Parameter]) -> None:
        """Initiate ParameterSampler object."""
        self.parameter = params
        assert isinstance(self.parameter, list)
        self.domain = np.array([param.domain for param in self.parameter])
        self._product_sampler = ProductSampler(
            [assign_sampler(param) for param in self.parameter]
        )

    @property
    def dimension(self) -> int:
        """Dimension of the parameters."""
        return self._product_sampler.dimension

    @property
    def mass(self) -> float:
        """Mass of the PDF."""
        return self._product_sampler.mass

    @property
    def maximum(self) -> float:
        """Maximum value of the PDF."""
        return self._product_sampler.maximum

    @property
    def mean(self) -> np.ndarray:
        """Mean of the PDF."""
        return self._product_sampler.mean

    @property
    def cov(self) -> np.ndarray:
        """Covariance of the PDF."""
        return self._product_sampler.cov

    def weight(self, x: np.ndarray) -> np.ndarray:
        """Weights of the parameter product PDF.

        Parameters
        ----------
        x : np.ndarray
            Evaluation points.

        Returns
        -------
        :
            Array of uniform weights for samples.
        """
        return self._product_sampler.weight(x)

    def pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of PDF evaluated in `x`.
        """
        return self._product_sampler.pdf(x)

    def log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate log-PDF.

        The log-PDF is given by the sum of the univariate log-PDFs.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of log-PDF evaluated in `x`.
        """
        return self._product_sampler.log_pdf(x)

    def grad_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate gradient of log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of gradient (vector valued) of log-PDF evaluated in `x`.
        """
        return self._product_sampler.grad_x_log_pdf(x)

    def hess_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate Hessian of log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of Hessian (matrix valued) of log-PDF evaluated in `x`.
        """
        return self._product_sampler.hess_x_log_pdf(x)

    def sample(self, shape: Union[int, List, Tuple, np.ndarray]) -> np.ndarray:
        """Draw samples from distribution.

        Parameters
        ----------
        shape : array_like
            Shape of the samples.

        Returns
        -------
        :
            Random samples of specified shape.
        """
        return self._product_sampler.sample(shape)


class WLSSampler(Sampler):
    """Weighted Least-Squares sampler as in Cohen & Migliorati 2017.

    Parameters
    ----------
    params : list of `pythia.parameter.Parameter`
        List of parameters.
    basis : list
        List of basis functions.
    tsa : bool, default=False
        Trial sampler adaptation. If True, a trial sampler is chosen on the
        distributions of parameters, if false a uniform trial sampler is used.

    Other Parameters
    ----------------
    trial_sampler : pythia.sampler.Sampler, default=None
        Trial sampler for rejection sampling. If `tsa` is true and either
        `trial_sampler` or `bulk` are `None`, the trial sampler is chosen
        automatically.
    bulk : float, defaul=None
        Scaling for trial sampler. If `tsa` is true and either
        `trial_sampler` or `bulk` are `None`, the trial sampler is chosen
        automatically.
    """

    def __init__(self,
                 params: List[pt.parameter.Parameter],
                 basis: List[Callable],
                 tsa: bool = True,
                 trial_sampler: Optional[Sampler] = None,
                 bulk: Optional[float] = None
                 ) -> None:
        """Initiate WLSSampler object."""
        self.parameter = params
        self._param_sampler = ParameterSampler(self.parameter)
        self.domain = self._param_sampler.domain
        self.basis = basis
        self._tsa = tsa
        if trial_sampler is None or bulk is None:
            self._trial_sampler, self._bulk = self._compute_trial_sampler()
        else:
            self._trial_sampler = trial_sampler
            self._bulk = bulk

    @property
    def dimension(self) -> int:
        """Dimension of the parameters."""
        return self._param_sampler.dimension

    @property
    def mass(self):
        """Mass of the PDF."""
        return 1

    @property
    def maximum(self) -> float:
        """Maximum value of the PDF."""
        return get_maximum(self.pdf, self.domain)

    @property
    def mean(self) -> np.ndarray:
        """Mean of the PDF."""
        raise NotImplementedError

    @property
    def cov(self) -> np.ndarray:
        """Covariance of the PDF."""
        raise NotImplementedError

    def weight(self, x: np.ndarray) -> np.ndarray:
        """Weights for the PDF.

        Parameters
        ----------
        x : array_like
            Points the weight function is evaluated in.

        Returns
        -------
        :
            weights of evaluation points `x`.
        """
        km = np.sum([abs(p(x))**2 for p in self.basis], axis=0)
        return len(self.basis) / km

    def pdf(self, x: np.ndarray) -> np.ndarray:
        """ Evaluate PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of PDF evaluated in `x`.
        """
        assert x.shape[-1] == self.dimension
        return self._param_sampler.pdf(x) / self.weight(x)

    def log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate log-PDF.

        The log-PDF is given by the sum of the univariate log-PDFs.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of log-PDF evaluated in `x`.
        """
        assert x.shape[-1] == self.dimension
        return self._param_sampler.log_pdf(x) - np.log(self.weight(x))

    def grad_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate gradient of log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of gradient (vector valued) of log-PDF evaluated in `x`.
        """
        raise NotImplementedError

    def hess_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate Hessian of log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of Hessian (matrix valued) of log-PDF evaluated in `x`.
        """
        raise NotImplementedError

    def _compute_trial_sampler(self) -> Tuple[Sampler, float]:
        """Trial sampler adaptation.

        Parameters
        ----------
        tsa : bool
            Adapt trial sampler or simply use uniform product sampler.

        Returns
        -------
        trial_sampler : pt.sampler.Sampler
            Trial sampler.
        bulk : array_like
            Domain estimate of the mass of the distribution.
        """
        sampler_list = []
        for param in self.parameter:
            if (self._tsa is True and param.distribution == "uniform"):
                sampler_list.append(BetaSampler(param.domain, 0.5, 0.5))
            else:
                sampler_list.append(UniformSampler(param.domain))
        trial_sampler = ProductSampler(sampler_list)
        bulk = get_maximum(
            lambda x: self.pdf(x)/trial_sampler.pdf(x), self.domain
        )
        return trial_sampler, bulk

    def sample(self, shape: Union[int, List, Tuple, np.ndarray]) -> np.ndarray:
        """Draw samples from distribution.

        Parameters
        ----------
        shape : array_like
            Shape of the samples.

        Returns
        -------
        :
            Random samples of specified shape.
        """
        if isinstance(shape, int):
            shape = (shape,)
        samples = rejection_sampling(
            self.pdf, self._trial_sampler, self._bulk, self.dimension, shape)
        return samples


class WLSTensorSampler(Sampler):
    """ WLS sampler for tensor multivariate basis.

    Sampler for weighted Least-Squares sampling as described by Cohen and
    Migliorati. Only full tensor space can be sampled. This allows for
    univariate weighted Least-Squares sampling in each component.

    Parameters
    ----------
    params : list of `pythia.parameter.Parameter`
        Parameter list.
    deg : list of int
        Polynomial degree of each component (same for all).
    tsa : bool, default=True
        Trial sampler adaptation. If True, a trial sampler is chosen on the
        distributions of parameters, if false a uniform trial sampler is
        used.
    """

    def __init__(self,
                 params: List[pt.parameter.Parameter],
                 deg: List[int],
                 tsa: bool = True
                 ) -> None:
        """ Initiate WLSTensorSampler object. """
        self.parameter = params
        self.deg = deg
        self.domain = np.array([param.domain for param in self.parameter])
        self._tsa = tsa
        # self._uBasis = pt.basis.univariate_basis(self.parameter, self.deg)
        # self._univariate_samplers = [assign_sampler(param)
        #                              for param in self.parameter]
        self._univariate_samplers = [WLSUnivariateSampler(
            p, d, self._tsa) for (p, d) in zip(self.parameter, self.deg)]
        self._product_sampler = ProductSampler(self._univariate_samplers)

    @property
    def dimension(self) -> int:
        """Dimension of the parameters."""
        return self._product_sampler.dimension

    @property
    def mass(self) -> float:
        """Mass of the PDF."""
        return self._product_sampler.mass

    @property
    def maximum(self) -> float:
        """Maximum value of the PDF."""
        return self._product_sampler.maximum

    @property
    def mean(self) -> np.ndarray:
        """Mean of the PDF."""
        return self._product_sampler.mean

    @property
    def cov(self) -> np.ndarray:
        """Covariance of the PDF."""
        return self._product_sampler.cov

    def weight(self, x: np.ndarray) -> np.ndarray:
        """Weights for the PDF.

        Parameters
        ----------
        x : array_like
            Points the weight function is evaluated in.

        Returns
        -------
        :
            Weights of evaluation points `x`.
        """
        assert x.shape[-1] == self.dimension
        weights = [s.weight for s in self._univariate_samplers]
        val = np.array(
            [weights[jj](x[..., jj]) for jj in range(self.dimension)])
        return np.prod(val, axis=0)

    def pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of PDF evaluated in `x`.
        """
        return self._product_sampler.pdf(x)

    def log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate log-PDF.

        The log-PDF is given by the sum of the univariate log-PDFs.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of log-PDF evaluated in `x`.
        """
        return self._product_sampler.log_pdf(x)

    def grad_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate gradient of log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of gradient (vector valued) of log-PDF evaluated in `x`.
        """
        return self._product_sampler.grad_x_log_pdf(x)

    def hess_x_log_pdf(self, x: np.ndarray) -> np.ndarray:
        """Evaluate Hessian of log-PDF.

        Parameters
        ----------
        x : array_like
            Evaluation points.

        Returns
        -------
        :
            Values of Hessian (matrix valued) of log-PDF evaluated in `x`.
        """
        return self._product_sampler.hess_x_log_pdf(x)

    def sample(self, shape: Union[int, List, Tuple, np.ndarray]) -> np.ndarray:
        """Draw samples from distribution.

        Parameters
        ----------
        shape : array_like
            Shape of the samples.

        Returns
        -------
        :
            Random samples of specified shape.
        """
        return self._product_sampler.sample(shape)


def rejection_sampling(pdf: Callable,
                       trial_sampler: Sampler,
                       scale: float,
                       dimension: int,
                       shape: Union[int, List, Tuple, np.ndarray],
                       ) -> np.ndarray:
    """Draw samples from pdf by rejection sampling.

    Parameters
    ----------
    pdf : Callable
        Probability density the samples are generated from.
    trial_sampler : Sampler
        Trial sampler proposal samples are drawn from.
    scale : float
        Threshold parameter with ``pdf <= scale * trialSampler.pdf``
    dimension : int
        Dimension of the (input of the) pdf.
    shape : array_like
        Shape of the samples.

    Returns
    -------
    :
        Random samples of specified shape.
    """
    if isinstance(shape, int):
        shape = (shape,)
    size = np.prod(np.array(shape))
    trial_samples = trial_sampler.sample(size)
    samples = np.empty_like(trial_samples)
    pointer = 0
    while pointer < size:
        trial_samples = trial_sampler.sample(size)
        checker = np.random.rand(trial_samples.shape[0])
        is_valid = (
            checker * max(scale, 1) * trial_sampler.pdf(trial_samples)
            <= pdf(trial_samples)
        )
        valid_samples = trial_samples[is_valid]
        start = pointer
        end = min(pointer+valid_samples.shape[0], size)
        samples[start:end] = valid_samples[0:min(
            valid_samples.shape[0], size-pointer)]
        pointer = end
    if dimension > 1:
        return np.moveaxis(samples.T.reshape(dimension, *shape), 0, -1)
    return samples.reshape(*shape)


def constraint_sampling(sampler: Sampler,
                        constraints: List[Callable],
                        shape: Union[int, List, Tuple, np.ndarray],
                        ) -> np.ndarray:
    """Draw samples according to algebraic constraints.

    Draw samples from target distribution and discard samples that do not
    satisfy the constraints.

    Parameters
    ----------
    sampler : Sampler
        Sampler to sample from.
    constraints : list of callable
        List of functions that return True if sample point satisfies the
        constraint.

    Returns
    -------
    :
        Samples drawn from sampler satisfying the constraints.

    Notes
    -----
    The constaints may lead to a non-normalized density function.
    """
    if isinstance(shape, int):
        shape = (shape,)
    samples = np.empty(sampler.sample(np.prod(shape)).shape)
    for j_sample in range(samples.shape[0]):
        proposal = sampler.sample((1,))
        met_constraints = np.all([c(proposal) for c in constraints])
        while not met_constraints:
            proposal = sampler.sample((1,))
            met_constraints = np.all([c(proposal) for c in constraints])
        samples[j_sample] = proposal
    return np.moveaxis(samples.T.reshape(sampler.dimension, *shape), 0, -1)


def assign_sampler(param: pt.parameter.Parameter) -> Sampler:
    """Assign a univariate sampler to the given parameter.

    Parameters
    ----------
    param : pythia.parameter.Parameter

    Returns
    -------
    :
        Univariate sampler.
    """
    if param.distribution == "uniform":
        return UniformSampler(param.domain)
    elif param.distribution == "normal":
        return NormalSampler(param.mean, param.var)
    elif param.distribution == "gamma":
        return GammaSampler(param.domain, param.alpha, param.beta)
    elif param.distribution == "beta":
        return BetaSampler(param.domain, param.alpha, param.beta)
    raise ValueError(f"unknown distribution '{param.distribution}'")


def get_maximum(f: Callable,
                domain: Union[List, Tuple, np.ndarray],
                n: int = 1000
                ) -> float:
    """Compute essential maximum of function by point evaluations.

    Parameters
    ----------
    f : callable
        Function to evaluate. Needs to map from n-dim space to 1-dim space.
    domain : array_like
        Domain to evaluate function on.
    n : int, default=1000
        Number of function evaluations. Evaluations are done on a uniform grid
        in domain. Actual number of points may thus be a little greater.

    Returns
    -------
    :
        Approximation of maximum of function `f`.
    """
    if not isinstance(domain, np.ndarray):
        domain = np.array(domain)
    assert domain.shape[-1] == 2 and domain.ndim == 2
    n_points = int(np.ceil(np.power(n, 1/domain.shape[0])))
    if domain.shape[0] > 1:
        eps = np.finfo(float).eps  # circumvent inf on bdry
        x = pt.misc.cartProd([
            np.linspace(dom[0]+eps, dom[1]-eps, n_points) for dom in domain]
        )
    else:
        x = np.linspace(domain[0, 0], domain[0, 1], n_points).reshape(-1, 1)
    return np.max(np.abs(f(x)))


if __name__ == "__main__":
    pass
