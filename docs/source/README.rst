
checkem: Check and Fix Outdated URLs
====================================


.. image:: https://badge.fury.io/py/checkem.svg
   :target: https://pypi.python.org/pypi/checkem/
   :alt: PyPI version fury.io


.. image:: https://zenodo.org/badge/336733328.svg
   :target: https://zenodo.org/badge/latestdoi/336733328
   :alt: DOI


.. image:: http://www.repostatus.org/badges/latest/active.svg
   :target: http://www.repostatus.org/#active
   :alt: Project Status
 

.. image:: https://codecov.io/gh/Nelson-Gon/checkem/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Nelson-Gon/checkem?branch=master
   :alt: Codecov


.. image:: https://github.com/Nelson-Gon/checkem/workflows/Test-Package/badge.svg
   :target: https://github.com/Nelson-Gon/checkem/workflows/Test-Package/badge.svg
   :alt: Test-Package


.. image:: https://travis-ci.com/Nelson-Gon/checkem.svg?branch=master
   :target: https://travis-ci.com/Nelson-Gon/checkem.svg?branch=master
   :alt: Travis Build


.. image:: https://img.shields.io/pypi/l/checkem.svg
   :target: https://pypi.python.org/pypi/checkem/
   :alt: PyPI license


.. image:: https://readthedocs.org/projects/checkem/badge/?version=latest
   :target: https://checkem.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


.. image:: https://img.shields.io/pypi/dm/checkem.svg
   :target: https://pypi.python.org/pypi/checkem/
   :alt: PyPI Downloads Month


.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://GitHub.com/Nelson-Gon/checkem/graphs/commit-activity
   :alt: Maintenance


.. image:: https://img.shields.io/github/last-commit/Nelson-Gon/checkem.svg
   :target: https://github.com/Nelson-Gon/checkem/commits/master
   :alt: GitHub last commit


.. image:: https://img.shields.io/github/issues/Nelson-Gon/checkem.svg
   :target: https://GitHub.com/Nelson-Gon/checkem/issues/
   :alt: GitHub issues


.. image:: https://img.shields.io/github/issues-closed/Nelson-Gon/checkem.svg
   :target: https://GitHub.com/Nelson-Gon/checkem/issues?q=is%3Aissue+is%3Aclosed
   :alt: GitHub issues-closed


``checkem`` aims to find all outdated URLs in a given file and fix them. 

**Supported file formats**

``checkem`` currently fixes URLs given a file of the following types:


* [x] MarkDown (.md)
* [x] Plain Text files (.txt)

**Installation**

The simplest way to install the latest release is as follows:

.. code-block:: shell

   pip install checkem

To install the development version:

Open the Terminal/CMD/Git bash/shell and enter

.. code-block:: shell


   pip install git+https://github.com/Nelson-Gon/checkem.git

   # or for the less stable dev version
   pip install git+https://github.com/Nelson-Gon/checkem.git@dev

Otherwise:

.. code-block:: shell

   # clone the repo
   git clone git@github.com:Nelson-Gon/checkem.git
   cd checkem
   python3 setup.py install

**Sample usage**

.. code-block:: python


   from checkem.checkem import checkmate as cm

**Replacing URLs written in .md format**

**Thank you very much**. 

To report any issues, suggestions or improvement, please do so 
at `issues <https://github.com/Nelson-Gon/checkem/issues>`_. 

..

   “Before software can be reusable it first has to be usable.” – Ralph Johnson


----

If you would like to cite this work, please use:

Nelson Gonzabato(2021) checkem: Check and Fix Outdated URLs https://github.com/Nelson-Gon/checkem
