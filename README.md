# nbforms

[![PyPI](https://img.shields.io/pypi/v/nbforms.svg)](https://pypi.org/project/nbforms/)
[![Run tests](https://github.com/chrispyles/nbforms/actions/workflows/run-tests.yml/badge.svg)](https://github.com/chrispyles/nbforms/actions/workflows/run-tests.yml)
[![codecov](https://codecov.io/github/chrispyles/nbforms/graph/badge.svg?token=GK2LAP9034)](https://codecov.io/github/chrispyles/nbforms)
[![Documentation Status](https://readthedocs.org/projects/nbforms/badge/?version=latest)](https://nbforms.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/chrispyles/nbforms/main?filepath=demo%2Fdemo.ipynb)

nbforms is a Python package designed to allow forms to be submitted by users such that the data they submit is immediately available for use in the notebook by the entire group. This is accomplished using ipywidgets and a shared web server, [nbforms-server](https://github.com/chrispyles/nbforms-server), that the Python client uploads its data to.

## Installation

To install the Python package, use pip:

```
pip install nbforms
```

## Documentation

The documentation for nbforms and nbforms-server can be found [here](https://nbforms.readthedocs.io/).
