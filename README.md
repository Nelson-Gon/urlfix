# checkem: Check and Fix Outdated URLs


[![PyPI version fury.io](https://badge.fury.io/py/checkem.svg)](https://pypi.python.org/pypi/checkem/)
[![DOI](https://zenodo.org/badge/336733328.svg)](https://zenodo.org/badge/latestdoi/336733328)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active) 
[![Codecov](https://codecov.io/gh/Nelson-Gon/checkem/branch/master/graph/badge.svg)](https://codecov.io/gh/Nelson-Gon/checkem?branch=master)
![Test-Package](https://github.com/Nelson-Gon/checkem/workflows/Test-Package/badge.svg)
![Travis Build](https://travis-ci.com/Nelson-Gon/checkem.svg?branch=master)
[![PyPI license](https://img.shields.io/pypi/l/checkem.svg)](https://pypi.python.org/pypi/checkem/)
[![Documentation Status](https://readthedocs.org/projects/checkem/badge/?version=latest)](https://checkem.readthedocs.io/en/latest/?badge=latest)
[![PyPI Downloads Month](https://img.shields.io/pypi/dm/checkem.svg)](https://pypi.python.org/pypi/checkem/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Nelson-Gon/checkem/graphs/commit-activity)
[![GitHub last commit](https://img.shields.io/github/last-commit/Nelson-Gon/checkem.svg)](https://github.com/Nelson-Gon/checkem/commits/master)
[![GitHub issues](https://img.shields.io/github/issues/Nelson-Gon/checkem.svg)](https://GitHub.com/Nelson-Gon/checkem/issues/)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/Nelson-Gon/checkem.svg)](https://GitHub.com/Nelson-Gon/checkem/issues?q=is%3Aissue+is%3Aclosed)



`checkem` aims to find all outdated URLs in a given file and fix them. 

**Supported file formats**

`checkem` currently fixes URLs given a file of the following types:

- [x] MarkDown (.md)
- [x] Plain Text files (.txt)


**Installation**

The simplest way to install the latest release is as follows:

```shell
pip install checkem

```

To install the development version:


Open the Terminal/CMD/Git bash/shell and enter

```shell

pip install git+https://github.com/Nelson-Gon/checkem.git

# or for the less stable dev version
pip install git+https://github.com/Nelson-Gon/checkem.git@dev

```

Otherwise:

```shell
# clone the repo
git clone git@github.com:Nelson-Gon/checkem.git
cd checkem
python3 setup.py install

```



**Sample usage**

```python

from checkem.checkem import checkmate as cm 

```

**Replacing URLs written in .md format**



**Thank you very much**. 

To report any issues, suggestions or improvement, please do so 
at [issues](https://github.com/Nelson-Gon/checkem/issues). 

> “Before software can be reusable it first has to be usable.” – Ralph Johnson

---

If you would like to cite this work, please use:

Nelson Gonzabato(2021) checkem: Check and Fix Outdated URLs https://github.com/Nelson-Gon/checkem


