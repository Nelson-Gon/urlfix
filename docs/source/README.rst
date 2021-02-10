
urlfix: Check and Fix Outdated URLs
===================================


.. image:: https://badge.fury.io/py/urlfix.svg
   :target: https://pypi.python.org/pypi/urlfix/
   :alt: PyPI version fury.io


.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.4515212.svg
   :target: https://doi.org/10.5281/zenodo.4515212
   :alt: DOI


.. image:: http://www.repostatus.org/badges/latest/active.svg
   :target: http://www.repostatus.org/#active
   :alt: Project Status
 

.. image:: https://codecov.io/gh/Nelson-Gon/urlfix/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Nelson-Gon/urlfix?branch=master
   :alt: Codecov


.. image:: https://github.com/Nelson-Gon/urlfix/workflows/Test-Package/badge.svg
   :target: https://github.com/Nelson-Gon/urlfix/workflows/Test-Package/badge.svg
   :alt: Test-Package


.. image:: https://travis-ci.com/Nelson-Gon/urlfix.svg?branch=master
   :target: https://travis-ci.com/Nelson-Gon/urlfix.svg?branch=master
   :alt: Travis Build


.. image:: https://img.shields.io/pypi/l/urlfix.svg
   :target: https://pypi.python.org/pypi/urlfix/
   :alt: PyPI license


.. image:: https://readthedocs.org/projects/urlfix/badge/?version=latest
   :target: https://urlfix.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


.. image:: https://img.shields.io/pypi/dm/urlfix.svg
   :target: https://pypi.python.org/pypi/urlfix/
   :alt: PyPI Downloads Month


.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://GitHub.com/Nelson-Gon/urlfix/graphs/commit-activity
   :alt: Maintenance


.. image:: https://img.shields.io/github/last-commit/Nelson-Gon/urlfix.svg
   :target: https://github.com/Nelson-Gon/urlfix/commits/master
   :alt: GitHub last commit


.. image:: https://img.shields.io/github/issues/Nelson-Gon/urlfix.svg
   :target: https://GitHub.com/Nelson-Gon/urlfix/issues/
   :alt: GitHub issues


.. image:: https://img.shields.io/github/issues-closed/Nelson-Gon/urlfix.svg
   :target: https://GitHub.com/Nelson-Gon/urlfix/issues?q=is%3Aissue+is%3Aclosed
   :alt: GitHub issues-closed


``urlfix`` aims to find all outdated URLs in a given file and fix them. 

**Supported file formats**

``urlfix`` fixes URLs given a file of the following types:


* [x] MarkDown (.md)
* [x] Plain Text files (.txt)

**Installation**

The simplest way to install the latest release is as follows:

.. code-block:: shell

   pip install urlfix

To install the development version:

Open the Terminal/CMD/Git bash/shell and enter

.. code-block:: shell


   pip install git+https://github.com/Nelson-Gon/urlfix.git

   # or for the less stable dev version
   pip install git+https://github.com/Nelson-Gon/urlfix.git@dev

Otherwise:

.. code-block:: shell

   # clone the repo
   git clone git@github.com:Nelson-Gon/urlfix.git
   cd urlfix
   python3 setup.py install

**Sample usage**

.. code-block:: python


   from urlfix import urlfix

**Replacing URLs written in .md format**

Given a file in which URLs are written in ``.md`` format, we can replace outdated URLs as follows:

.. code-block:: python


   urlfix.replace_urls("testurls.md")

The above uses default arguments and will not replace a file inplace. This is a safety mechanism to ensure one does not
damage their files. By default, files are written to a ``replacement.txt`` file which can be overridden with the name of 
choice.

If you are confident enough, you can simply set ``inplace`` to ``True``.

.. code-block:: python

   urlfix.replace_urls("testurls.md", inplace=True)

**Thank you very much**. 

To report any issues, suggestions or improvement, please do so 
at `issues <https://github.com/Nelson-Gon/urlfix/issues>`_. 

..

   “Before software can be reusable it first has to be usable.” – Ralph Johnson


----

If you would like to cite this work, please use:

Nelson Gonzabato(2021) urlfix: Check and Fix Outdated URLs https://github.com/Nelson-Gon/urlfix
