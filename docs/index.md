<!-- .. nbforms documentation master file, created by
   sphinx-quickstart on Fri Jan 24 22:12:36 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive. -->

# Welcome to nbforms's documentation

```eval_rst
.. toctree::
   :maxdepth: 1
   :caption: Contents:
   :hidden:

   install_deploy
   notebook_usage
   attendance
   auth
   API Reference <nbforms>
```

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/chrispyles/nbforms/master?filepath=demo%2Fdemo.ipynb)

nbforms is a Python package designed to allow forms to be submitted by users such that the data they submit is immediately available for use in the notebook by the entire group. This is accomplished using ipywidgets and a Heroku-deployable Sinatra webapp, nbforms-server, that collects submissions from HTTP requests and stores them, differentiating by a notebook identifier.
