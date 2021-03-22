# Welcome to urlfix's changelog 

**urlfix 0.2.1**

* Download URL is now automated, please release new version as `v-version-number-here`.

* Script mode has been added as a `__main__.py` module. You can now therefore call `urlfix` at the command line/Terminal 
  via `python -m urlfix`.

* A script mode has been added to enable commandline replacement of outdated links. See
  [#22](https://github.com/Nelson-Gon/urlfix/issues/22). 

* Fixed issues with links not being replaced following changes to directory replacement. 

* Restored inplace replacement. Using temporary files for now. See 
  [#15](https://github.com/Nelson-Gon/urlfix/pull/15) and [#10](https://github.com/Nelson-Gon/urlfix/issues/10).

* Versioning is now automated. You can now check version number via `urlfix.__version__`

* `dirurlfix` is a new module dedicate to directory replacements. 

* Fixed issues with markdown links in the format `[]()[]()` not being fully matched. 
 See [#17](https://github.com/Nelson-Gon/urlfix/issues/17)

* Fixed issues with double text appearing in the replacement file. 
  Related to [Issue 20](https://github.com/Nelson-Gon/urlfix/issues/20). 

* Fixed issues with URLs not being matched if they are on the same line. 
  Issue [#20](https://github.com/Nelson-Gon/urlfix/issues/20). 

* Users are now warned if a target URL is outdated and no newer URL exists. 
  See [#18](https://github.com/Nelson-Gon/urlfix/issues/18)

* Fixed issues with text loss in output markdown files. See [#16](https://github.com/Nelson-Gon/urlfix/issues/16) 

* Fixed issues with tests failing when run [consecutively](https://github.com/Nelson-Gon/urlfix/pull/13) 

* Inplace replacement is no longer supported via the `inplace=True` argument. 

* Replacement of files now supports adding exceptions that is URLs whose links are known to be valid. 

* Added support for automatic detection of file extensions negating the need to manually specify file formats. 

* Initial support for directory replacements, thanks to [nirolada](https://github.com/nirolada). 

**urlfix 0.2.0**

* `show_parsed_urls` was dropped. Future plans to find a better way to validate matched URLs.

* `find_links` was dropped. Everything is now done under `replace_urls`.

* `URLFix` is a new class to make it easier to write class methods and access class variables.

* `show_parsed_urls` is no longer necessary and may be dropped in future versions. 

* `replace_urls` was refactored to avoid unnecessary loops that would otherwise slow down the process.

* Extended sanity tests to ensure that input and output files exist. 

* `returned_matched` was dropped in `replace_urls`. Use `show_parsed_urls` for low level returns. 

* `verbose` in `replace_urls` is now more human friendly by providing the actual name of the output file.

* Updated `testurls.md` to ensure only markdown like links are replaced.

* The regular expression in `find_links` was replaced with a more robust one. 

* `visit_urls` was renamed to `replace_urls` and extended to allow inplace replacement (or not)
 as well as writing to an output file.
  
* `fixurls` was renamed to `urlfix`.

* `check_url` was removed but may be replaced. 

* Add more sanity checks to ensure that the regular expressions used work as detected.

* Made expected formats and return types more explicit. 

* Initial support for tests. 

* Fixed issues with installation


**urlfix 0.1.0**

* Initial release to preserve name on PyPI.



