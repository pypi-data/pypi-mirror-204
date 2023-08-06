![PyThia Logo Full](logo/logo_full_transparent.png)

# PyThia Uncertainty Quantification Toolbox

The PyThia UQ toolbox uses polynomial chaos surrogates to efficiently generate a surrogate of any (parametric) forward problem.
The surrogate is fast to evaluate, allows analytical differentiation and has a built-in global sensitivity analysis via Sobol indices.
Assembling the surrogate is done non-intrusive by least-squares regression, hence only training pairs of parameter realizations and evaluations of the forward problem are required to construct the surrogate.
No need to compute any nasty interfaces for lagacy code.

## Why the Name?

Pythia was the title of the high priestess of the temple of Apollo in Delphi.
Hence you could say she used her prophetic abilities to quantify which was uncertain.
Moreover, the package is written in python, so...

## Installation

The latest stable version of PyThia can be installed using pip
```shell.
pip install pythia-uq
```
To install PyThia from source, i.e., if you want to work with the latest (and possibly unstable) changes, simply clone the repository and run the setup script to install PyThia to any environment
```shell
cd path/to/pythia-repo/
pip install .
```
PyThia can then be imported from any location with `import pythia`.

## Documentation

The documentation of the stable package version can be found here: [pythia-uq.rtfd.io](https://pythia-uq.rtfd.io).
For other versions of the documentation, see [https://readthedocs.org/projects/pythia-uq/](https://readthedocs.org/projects/pythia-uq/).

## How to cite PyThia

There is no official related article to cite PyThia yet.
If you make use of PyThia in a publication, please use the meta data from the `CITATION.cff` file or cite it with a BibTeX entry similar to this:
```bibtex
@software{pythia,
    author = {Farchmin, Nando and Heidenreich, Sebastian},
    title = {PyThia UQ Toolbox},
    version = {3.1.0},
    url = {https://pythia-uq.readthedocs.io/en/v3.1.0/},
    year = {2022},
    month = {12}
}
```

## Want to contribute?

Check out the [contribution guidelines](CONTRIBUTING.md) on how to create issues or file bug reports and feature requests.
Or ever better start developping the PyThia project yourself after reading the [development guidelines](DEVELOPERS.md).

## License
This work is dual-licensed under GNU Lesser General Public License v3.0 or later and Hippocratic License 3.0 or later.
You can choose between one of them if you use this work.

`SPDX-License-Identifier: LGPL-3.0-or-later OR Hippocratic-3.0-ECO-MEDIA-MIL`

## Funding

The development of PyThia UQ Toolbox vers. 1 and 2 has been funded by the German Central Innovation Program (ZIM) No. ZF4014017RR7.
The development of PyThia UQ Toolbox vers. 3 has been funded by the EMPIR project 20IND04-ATMOC.

## References

Here we list the papers that describe concepts implemented in **PyThia** for the interested user.
In principle **PyThia** uses a (sparse) polynomial chaos expansion to construct a surrogate of any function via least-squares regression.
We first applied the **PyThia** software package to analyse the sensitivities of a scatterometry experiment [^pythia-scat-A] using global sensitivity analysis via Sobol indices [^sobol-indices].
We also solved the inverse problem for the same experiment [^pythia-scat-B] via Bayesian inversion.
To use a minimal but still sufficient amount of random samples for the regression, we integrated weighted least-squares sampling [^wls-sampling] into **PyThia**.

[^pythia-scat-A]: [An efficient approach to global sensitivity analysis and parameter estimation for line gratings](https://arxiv.org/abs/1910.14435)
[^pythia-scat-B]: [Efficient Bayesian inversion for shape reconstruction of lithography masks](https://arxiv.org/abs/2005.05164)
[^sobol-indices]: [Global sensitivity analysis using polynomial chaos expansions](https://www.sciencedirect.com/science/article/abs/pii/S0951832007001329)
[^wls-sampling]: [Optimal weighted least-squares methods](https://arxiv.org/abs/1608.00512)

