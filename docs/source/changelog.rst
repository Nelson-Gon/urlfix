
Welcome to urlfix's changelog
=============================

**urlfix 0.2.1**


* Initial support for directory replacements, thanks to `nirolada <https://github.com/nirolada>`_. 

**urlfix 0.2.0**


* 
  ``show_parsed_urls`` was dropped. Future plans to find a better way to validate matched URLs.

* 
  ``find_links`` was dropped. Everything is now done under ``replace_urls``.

* 
  ``URLFix`` is a new class to make it easier to write class methods and access class variables.

* 
  ``show_parsed_urls`` is no longer necessary and may be dropped in future versions. 

* 
  ``replace_urls`` was refactored to avoid unnecessary loops that would otherwise slow down the process.

* 
  Extended sanity tests to ensure that input and output files exist. 

* 
  ``returned_matched`` was dropped in ``replace_urls``. Use ``show_parsed_urls`` for low level returns. 

* 
  ``verbose`` in ``replace_urls`` is now more human friendly by providing the actual name of the output file.

* 
  Updated ``testurls.md`` to ensure only markdown like links are replaced.

* 
  The regular expression in ``find_links`` was replaced with a more robust one. 

* 
  ``visit_urls`` was renamed to ``replace_urls`` and extended to allow inplace replacement (or not)
  as well as writing to an output file.

* 
  ``fixurls`` was renamed to ``urlfix``.

* 
  ``check_url`` was removed but may be replaced. 

* 
  Add more sanity checks to ensure that the regular expressions used work as detected.

* 
  Made expected formats and return types more explicit. 

* 
  Initial support for tests. 

* 
  Fixed issues with installation

**urlfix 0.1.0**


* Initial release to preserve name on PyPI.
