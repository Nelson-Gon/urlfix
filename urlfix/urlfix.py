from collections.abc import Sequence
import os
from pathlib import Path
import re
import urllib.request
from urllib.request import Request
from urllib.error import URLError
import warnings


class URLFix(object):
    def __init__(self, input_file, output_file=None):
        """
        :param input_file: Path to input_file
        :param output_file: Path to output_file
        """
        self.input_file = input_file
        self.output_file = output_file
        # automatically detect input file format
        format_pattern = r'.+\.(\w+)'
        matches = re.findall(format_pattern, self.input_file)
        self.input_format = matches[0] if len(matches) > 0 else ''

    def replace_urls(self, verbose=False, correct_urls=None):
        """
        :param verbose Logical. Should you be notified of what URLs have moved? Defaults to False.
        :param correct_urls. A sequence of urls known to be correct.
        :return  Replaces outdated URL and writes to the specified file. It also returns the number of URLs that have
        changed. The latter is useful for tests.
        """
        if self.input_format not in ("md", "txt"):
            raise NotImplementedError(f"File format {self.input_format} is not yet supported.")
        else:
            pass

        link_text = "[^]]+"
        # Better markdown link matching  taken from https://stackoverflow.com/a/23395483/10323798
        # http:// or https:// followed by anything but a closing paren
        actual_link = "http[s]?://[^)|^\s|?<=\]]+"
        # Need to find more links if using double bracket Markdown hence define single md []() RegEx.
        single_md = "\[([^]]+)\]\((http[s]?://[^\s|^\)]+)\)"
        combined_regex = f"\[({link_text})\]\(({(actual_link)})\)\]\((http[s].*)\)|({single_md})"
        # Match only links in a text file, do not text that follows.
        # Assumes that links will always be followed by a space.
        final_regex = "http[s]?://[^\s]+" if self.input_format == "txt" else combined_regex

        if self.output_file is None:
            raise ValueError("Please provide an output file to write to.")
        output_file = self.output_file

        if not all(os.path.isfile(x) for x in [self.input_file, output_file]):
            raise FileNotFoundError("input_file and output_file should be valid files.")

        number_moved = 0
        number_of_urls = 0

        with open(self.input_file, "r") as input_f, open(output_file, "w") as out_f:
            for line in input_f:
                matched_url = re.findall(final_regex, line)
                # Drop empty strings
                if self.input_format == "md":
                    matched_url = [list(str(x) for x in texts_links if x != '') for texts_links in matched_url]
                    for link_texts in matched_url:
                        if len(link_texts) > 1:
                            link_texts = link_texts[1:]
                            # This is used because for some reason we match links twice if single md []()
                            # This isn't ideal
                            # TODO: Use better Regular Expression that matches the target links at once
                            matched_url = list(filter(lambda x: ("https" or "http") in x, link_texts))
                if len(matched_url) == 0:
                    # If no URL found, write this line so it is kept in the output file.
                    out_f.write(line)
                    pass
                else:


                        for final_link in matched_url:
                            number_of_urls += 1
                            if isinstance(correct_urls, Sequence) and final_link in correct_urls:
                                # skip current url if it's in 'correct_urls'
                                print(f'{final_link} is already valid.')
                                continue

                            # This printing step while unnecessary may be useful to make sure things work as expected
                            if verbose:
                                print(f"Found {final_link} in {input_f.name}, now validating.. ")
                            try:
                                visited_url = urllib.request.urlopen(
                                    Request(final_link, headers={'User-Agent': 'XYZ/3.0'}))
                            except URLError as err:
                                # TODO: Figure out why getting the error code fails.
                                # Leave intact
                                warnings.warn(f"{final_link} not updated. Reason: {err.reason}")
                                # Must be a way to skip, for now rewrite it in there
                                pass
                            else:
                                url_used = visited_url.geturl()
                                if url_used != final_link:
                                    number_moved += 1
                                    if verbose:
                                        print(f"{final_link} replaced with {url_used} in {out_f.name}")
                                    line.replace(final_link, url_used)
                        out_f.write(line)
        information = "URLs have changed" if number_moved != 1 else "URL has changed"
        print(f"{number_moved} {information} of the {number_of_urls} links found in {self.input_file}")
        return number_moved


class DirURLFix(object):
    def __init__(self, input_dir):
        """
        :param input_dir: Path to input_dir.
        """
        self.input_dir = input_dir
        self.use_files = Path(self.input_dir)

    def __replace_by_format(self, _format, **kwargs):
        """
        :param _format: Input format of the files. Currently supports md and txt
        :return: File with outdated URLs replaced.
        """

        for input_file in self.use_files.glob(f'*.{_format}'):
            input_file = str(input_file)  # convert object to path string
            if '_output' in input_file:
                print(f"File is a fix of another file: {input_file}")
                continue  # skip output files

            output_file = input_file.replace(f'.{_format}', f'_output.{_format}')
            if os.path.exists(output_file):
                print(f"File already fixed: {input_file}")
                continue  # skip file that's already been fixed

            with open(output_file, 'w'):
                pass  # create an empty output file
            return URLFix(input_file, output_file).replace_urls(**kwargs)

    def replace_urls(self, **kwargs):
        if not os.path.exists(self.input_dir):
            raise OSError('Path does not exist!')
        if not os.path.isdir(self.input_dir):
            raise NotADirectoryError('Input path must be a directory!')
        number_moved = []
        for _format in ('md', 'txt'):
            for file_found in list(self.use_files.glob(f"*.{_format}")):
                number_moved.append(self.__replace_by_format(_format, **kwargs))

        print('All files have been updated, thank you for using urlfix.')
        return number_moved
