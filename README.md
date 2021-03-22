# urlfix: Check and Fix Outdated URLs


[![PyPI version fury.io](https://badge.fury.io/py/urlfix.svg)](https://pypi.python.org/pypi/urlfix/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4515212.svg)](https://doi.org/10.5281/zenodo.4515212)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active) 
[![Codecov](https://codecov.io/gh/Nelson-Gon/urlfix/branch/master/graph/badge.svg)](https://codecov.io/gh/Nelson-Gon/urlfix?branch=master)
![Test-Package](https://github.com/Nelson-Gon/urlfix/workflows/Test-Package/badge.svg)
![Travis Build](https://travis-ci.com/Nelson-Gon/urlfix.svg?branch=master)
[![PyPI license](https://img.shields.io/pypi/l/urlfix.svg)](https://pypi.python.org/pypi/urlfix/)
[![Documentation Status](https://readthedocs.org/projects/urlfix/badge/?version=latest)](https://urlfix.readthedocs.io/en/latest/?badge=latest)
[![Total Downloads](https://pepy.tech/badge/urlfix)](https://pepy.tech/project/urlfix)
[![Monthly Downloads](https://pepy.tech/badge/urlfix/month)](https://pepy.tech/project/urlfix)
[![Weekly Downloads](https://pepy.tech/badge/urlfix/week)](https://pepy.tech/project/urlfix)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Nelson-Gon/urlfix/graphs/commit-activity)
[![GitHub last commit](https://img.shields.io/github/last-commit/Nelson-Gon/urlfix.svg)](https://github.com/Nelson-Gon/urlfix/commits/master)
[![GitHub issues](https://img.shields.io/github/issues/Nelson-Gon/urlfix.svg)](https://GitHub.com/Nelson-Gon/urlfix/issues/)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/Nelson-Gon/urlfix.svg)](https://GitHub.com/Nelson-Gon/urlfix/issues?q=is%3Aissue+is%3Aclosed)



`urlfix` aims to find all outdated URLs in a given file and fix them. 

**Supported file formats**

`urlfix` fixes URLs given a file of the following types:

- [x] MarkDown (.md)
- [x] Plain Text files (.txt)

- [ ] ReStructured Text (.rst)

- [ ] PDF (.pdf)

- [ ] Word (.docx)

- [ ] ODF (.odf)

**Features List**

- [x] Commandline and programmer-friendly modes. 

- [x] Replace outdated URLs/links in a single file

- [x] Replace outdated URLs/links in a directory

- [x] Replace outdated URLs/links in the same file or in the same files in a directory i.e inplace.

- [ ] Replace files in nested directories

**Installation**

The simplest way to install the latest release is as follows:

```shell
pip install urlfix

```

To install the development version:


Open the Terminal/CMD/Git bash/shell and enter

```shell

pip install git+https://github.com/Nelson-Gon/urlfix.git

# or for the less stable dev version
pip install git+https://github.com/Nelson-Gon/urlfix.git@dev

```

Otherwise:

```shell
# clone the repo
git clone git@github.com:Nelson-Gon/urlfix.git
cd urlfix
python3 setup.py install

```



**Sample usage**

**Script Mode**

To use at the commandline, please use:

```shell

python -m urlfix --mode "f" --verbose 1 --inplace 1 --input-file myfile.md

```

If not replacing within the same file, then:

```shell

python -m urlfix --mode "f" --verbose 1 --inplace 0 --input-file myfile.md --output-file myoutputfile.md

```



To get help:

```shell
python -m urlfix -h 

#usage: main.py [-h] -m MODE -in INPUT_FILE [-o OUTPUT_FILE] -v {False,false,0,True,true,1} -i {False,false,0,True,true,1}
#
#optional arguments:
#  -h, --help            show this help message and exit
#  -m MODE, --mode MODE  Mode to use. One of f for file or d for directory
#  -in INPUT_FILE, --input-file INPUT_FILE
#                        Input file for which link updates are required.
#  -o OUTPUT_FILE, --output-file OUTPUT_FILE
#                        Output file to write to. Optional, only necessary if not replacing inplace
#  -v {False,false,0,True,true,1}, --verbose {False,false,0,True,true,1}
#                        String to control verbosity. Defaults to True.
#  -i {False,false,0,True,true,1}, --inplace {False,false,0,True,true,1}
#                        Should links be replaced inplace? This should be safe but to be sure, test with an output file first.



```

**Programmer-Friendly Mode**

```python

from urlfix.urlfix import URLFix
from urlfix.dirurlfix import DirURLFix

```

**Create an object of class URLFix**

```python

urlfix_object = URLFix("testfiles/testurls.txt", output_file="replacement.txt")

```
**Replacing URLs**

After creating our object, we can replace outdated URLs as follows:

```python

urlfix_object.replace_urls(verbose=1)

```
The above uses default arguments and will not replace a file inplace. This is a safety mechanism to ensure one does not
damage their files. 

Since we set `verbose` to `True`, we get the following output:

```shell
urlfix_object.replace_urls()
Found https://www.r-pkg.org/badges/version/manymodelr in testurls.txt, now validating.. 
Found https://cran.r-project.org/package=manymodelr in testurls.txt, now validating.. 
https://cran.r-project.org/package=manymodelr replaced with https://cran.r-project.org/web/packages/manymodelr/index.html 
in replacement.txt
Found https://tidyverse.org/lifecycle/#maturing in testurls.txt, now validating.. 
https://tidyverse.org/lifecycle/#maturing replaced with https://lifecycle.r-lib.org/articles/stages.html in 
replacement.txt
2 URLs have changed of the 3 links found in testurls.txt
2

```

To replace silently, simply set verbose to `False` (which is the default). 

```python
urlfix_object.replace_urls()
2 URLs have changed of the 3 links found in testurls.txt
2
```

If there are URLs known to be valid, pass these to the `correct_urls` argument to save some time.

```python 

urlfix_object.replace_urls(correct_urls=[urls_here]) # Use a Sequence eg tuple, list, etc

```


**Replacing several files in a directory**

To replace several files in a directory, we can use `DirURLFix` as follows.

* Instantiate an object of class `DirURLFix`

```python

replace_in_dir = DirURLFix("path_to_dir")

```

* Call `replace_urls`

```python

replace_in_dir.replace_urls()

```

---

To report any issues, suggestions or improvement, please do so at [issues](https://github.com/Nelson-Gon/urlfix/issues). 

If you would like to cite this work, please use:

Nelson Gonzabato (2021) urlfix: Check and Fix Outdated URLs https://github.com/Nelson-Gon/urlfix


**Thank you very much**. 


> “Before software can be reusable it first has to be usable.” – Ralph Johnson






