.. _installation:

Installation
============

unbaffeld is designed to be used directly from the repository, or from the
standard python setuptools build system.    The documentation is designed with
both workflows in mind, but here we discuss the standard setuptools system.

To build and install unbaffeld, the steps are::

    python setup.py build
    python setup.py install

The installation directory by default is the site-packages directory for the
python used in the above command.  To specify a different location::

    python setup.py --prefix=<path to installation> install
