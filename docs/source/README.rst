
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


.. image:: https://pepy.tech/badge/urlfix
   :target: https://pepy.tech/project/urlfix
   :alt: Total Downloads


.. image:: https://pepy.tech/badge/urlfix/month
   :target: https://pepy.tech/project/urlfix
   :alt: Monthly Downloads


.. image:: https://pepy.tech/badge/urlfix/week
   :target: https://pepy.tech/project/urlfix
   :alt: Weekly Downloads


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

**Features List**


* 
  [x] Commandline and programmer-friendly modes. 

* 
  [x] Replace outdated URLs/links in a single file

* 
  [x] Replace outdated URLs/links in a directory

* 
  [x] Replace outdated URLs/links in the same file or in the same files in a directory i.e. inplace.

* 
  [x] Replace outdated links in files in nested directories

* [x] Replace outdated links in files in sub-nested directories 

**Supported file formats**

``urlfix`` fixes URLs given a file of the following types:


* [x] MarkDown (.md)
* 
  [x] Plain Text files (.txt)

* 
  [x] RMarkdown (.rmd)

* 
  [x] ReStructured Text (.rst)

* 
  [ ] PDF (.pdf)

* 
  [ ] Word (.docx)

* 
  [ ] ODF (.odf)

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

**Script Mode**

To use at the commandline, please use:

.. code-block:: shell


   python -m urlfix --mode "f" --verbose 1 --inplace 1 --inpath myfile.md

If not replacing within the same file, then:

.. code-block:: shell


   python -m urlfix --mode "f" --verbose 1 --inplace 0 --inpath myfile.md --output-file myoutputfile.md

To get help:

.. code-block:: shell

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

**Programmer-Friendly Mode**

.. code-block:: python


   from urlfix.urlfix import URLFix
   from urlfix.dirurlfix import DirURLFix

**Create an object of class URLFix**

.. code-block:: python


   urlfix_object = URLFix("testfiles/testurls.txt", output_file="replacement.txt")

**Replacing URLs**

After creating our object, we can replace outdated URLs as follows:

.. code-block:: python


   urlfix_object.replace_urls(verbose=1)

The above uses default arguments and will not replace a file inplace. This is a safety mechanism to ensure one does not
damage their files. 

Since we set ``verbose`` to ``True``\ , we get the following output:

.. code-block:: python

   urlfix_object.replace_urls()

To replace silently, simply set verbose to ``False`` (which is the default). 

.. code-block:: python

   urlfix_object.replace_urls()

If there are URLs known to be valid, pass these to the ``correct_urls`` argument to save some time.

.. code-block:: python


   urlfix_object.replace_urls(correct_urls=[urls_here]) # Use a Sequence eg tuple, list, etc

**Replacing several files in a directory**

To replace several files in a directory, we can use ``DirURLFix`` as follows.


* Instantiate an object of class ``DirURLFix``

.. code-block:: python


   replace_in_dir = DirURLFix("path_to_dir")


* Call ``replace_urls``

.. code-block:: python


   replace_in_dir.replace_urls()

**Recursively replacing links in nested directories**

To replace outdated links in several files located in several directories, we set ``recursive`` to ``True``.
Currently, replacing links in directories nested within nested directories is not (yet) supported.

.. code-block:: python


   recursive_object = DirURLFix("path_to_root_directory", recursive=True)

We can then proceed as above

.. code-block:: python


   recursive_object.replace_urls() # provide other arguments as you may wish.

----

To report any issues, suggestions or improvement, please do so at `issues <https://github.com/Nelson-Gon/urlfix/issues>`_. 

If you would like to cite this work, please use:

Nelson Gonzabato (2021) urlfix: Check and Fix Outdated URLs https://github.com/Nelson-Gon/urlfix

**Thank you very much**. 

..

   “Before software can be reusable it first has to be usable.” – Ralph Johnson

