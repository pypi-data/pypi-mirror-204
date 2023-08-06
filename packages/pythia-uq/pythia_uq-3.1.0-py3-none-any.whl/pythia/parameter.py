"""PyThia classes containing Parameter information.

SPDX-License-Identifier: LGPL-3.0-or-later OR Hippocratic-3.0-ECO-MEDIA-MIL
"""
from typing import List, Tuple, Optional, Union
from dataclasses import dataclass
import numpy as np


@dataclass
class Parameter:
    """ Class used for stochasic parameters.

    Parameters
    ----------
    index : int
        Enumeration index of the parameter.
    name : str
        Parameter name.
    domain : array_like
        Supported domain of the parameter distribution.
    distribution : str
        Distribution identifier of the parameter.
    mean : float, default=None
        Mean of parameter probability.
    var : float, default=None
        Variance of parameter probability.
    alpha : float, default=None
        Alpha value of Beta and Gamma distribution.
    beta : float, default=None
        Beta value of Beta and Gamma distribution.
    """
    index: int
    name: str
    domain: Union[List, Tuple, np.ndarray]
    distribution: str
    mean: Optional[float] = None
    var: Optional[float] = None
    alpha: Optional[float] = None
    beta: Optional[float] = None

    def __post_init__(self) -> None:
        """Sanity checks."""
        assert isinstance(self.index, int)
        assert isinstance(self.name, str)
        assert isinstance(self.distribution, str)

        self.domain = np.array(self.domain)
        assert self.domain.shape == (2,)

        if self.distribution == "uniform":
            assert self.mean is None
            assert self.var is None
            assert self.alpha is None
            assert self.beta is None
        elif self.distribution == "normal":
            assert isinstance(self.mean, (float, int))
            assert isinstance(self.var, (float, int))
            assert self.var > 0
            assert self.alpha is None
            assert self.beta is None
        elif self.distribution in ["gamma", "beta"]:
            assert self.mean is None
            assert self.var is None
            assert isinstance(self.alpha, (float, int))
            assert isinstance(self.beta, (float, int))
            assert self.alpha >= 0
            assert self.beta >= 0
        else:
            raise ValueError(f"Unknown distribution: '{self.distribution}'")
