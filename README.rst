pyMentalModels
==============
|Docs_|
pyMentalModels is a Python implementation of the Mental Model Theory.

A WebApp with a preliminary version can be found at https://modalmentalmodel.herokuapp.com

A convenience script is also provided.

.. |Docs_| image:: https://readthedocs.org/projects/pyMentalModels/badge/?version=latest
   :target: http://pymentalmodels.readthedocs.io/en/latest/
   :alt: Docs

Installation
============
LINUX instructions
------------------

Requirements are PYTHON 3(any) and sympy library.
Set up a python virtualenv:

```
$ virtualenv .env
```

source it:

```
$ source .env/bin/activate
```

and run:

```
$ pip install git+https://github.com/MRocholl/pyMentalModels.git
```

WINDOWS instructions
--------------------

Anaconda is the easiest way to enable scientific python on windows.
It can be downloaded at:

    https://www.anaconda.com/download/#windows 

    !! Make sure to download the version for **python 3**

The required package `sympy` is included by default.

How To run the script
=====================

A command line interface is provided.
Run the script with 

```
$ mental-models
```
