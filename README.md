# qosst-skr

<center>

![QOSST Logo](qosst_logo_full.png)

<a href='https://qosst-skr.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/qosst-skr/badge/?version=latest' alt='Documentation Status' />
</a>
<a href="https://github.com/qosst/qosst-skr/blob/main/LICENSE"><img alt="Github - License" src="https://img.shields.io/github/license/qosst/qosst-skr"/></a>
<a href="https://github.com/qosst/qosst-skr/releases/latest"><img alt="Github - Release" src="https://img.shields.io/github/v/release/qosst/qosst-skr"/></a>
<a href="https://pypi.org/project/qosst-skr/"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/qosst-skr"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/pylint-dev/pylint"><img alt="Linting with pylint" src="https://img.shields.io/badge/linting-pylint-yellowgreen"/></a>
<a href="https://mypy-lang.org/"><img alt="Checked with mypy" src="https://www.mypy-lang.org/static/mypy_badge.svg"></a>
<a href="https://img.shields.io/pypi/pyversions/qosst-skr">
    <img alt="Python Version" src="https://img.shields.io/pypi/pyversions/qosst-skr">
</a>
<img alt="Docstr coverage" src=".docs_badge.svg" />
</center>
<hr/>

This project is part of [QOSST](https://github.com/qosst/qosst).

## Features

`qosst-skr` is the project that holds the codes to compute the Secret Key Rate (SKR) in different cases. For now, the SKR can be computed in the following cases:

* Gaussian Trusted Heterodyne Asymptotic;
* Gaussian Trusted Homodyne Asymptotic;
* Gaussian Untrusted Homodyne Asymptotic.

## Installation

The module can be installed with the following command:

```console
pip install qosst-skr
```

It is also possible to install it directly from the github repository:

```console
pip install git+https://github.com/qosst/qosst-skr
```

It also possible to clone the repository before and install it with pip or poetry

```console
git clone https://github.com/qosst/qosst-skr
cd qosst-skr
poetry install
pip install .
```

## Documentation

The whole documentation can be found at https://qosst-skr.readthedocs.io/en/latest/

## Usage

`qosst-skr` can be used by importing the functions and using the `skr` static method from each class. The parameters depends on the considered case.

```python
from qosst_skr.gaussian_trusted_heterodyne_asymptotic import GaussianTrustedHeterodyneAsymptotic

k = GaussianTrustedHeterodyneAsymptotic(Va=5, eta=0.5, Vel=0.1, xi=0.01, T=0.5)
```

Refer to the documentation for more information.

## License

As for all submodules of QOSST, `qosst-skr` is shipped under the [Gnu General Public License v3](https://www.gnu.org/licenses/gpl-3.0.html).

## Contributing

Contribution are more than welcomed, either by reporting issues or proposing merge requests. Please check the contributing section of the [QOSST](https://github.com/qosst/qosst) project fore more information.
