import urllib.request
import re
from urllib.request import Request
import os
from pathlib import Path


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


    def replace_urls(self, inplace=False, verbose=False):
        """
        :param inplace Logical. Determines if you need to replace URLs inplace. Defaults to False.
        :param verbose Logical. Should you be notified of what URLs have moved? Defaults to False.
        :return  Replaces outdated URL and writes to the specified file. It also returns the number of URLs that have
        changed. The latter is useful for tests.
        """
        link_text = "[^]]+"
        # Better markdown link matching  taken from https://stackoverflow.com/a/23395483/10323798
        # http:// or https:// followed by anything but a closing paren
        actual_link = "http[s]?://[^)]+"
        combined_regex = f"\[({link_text})]\(\s*({actual_link})\s*\)"
        # Match only links in a text file, do not text that follows.
        # Assumes that links will always be followed by a space.
        final_regex = "http[s]?://[^\s]+" if self.input_format == "txt" else combined_regex

        number_moved = 0
        if inplace:
            output_file = self.input_file
        else:
            if self.output_file is None:
                raise ValueError("Please provide an output file to write to.")
            output_file = self.output_file

        if not all(os.path.isfile(x) for x in [self.input_file, output_file]):
            raise FileNotFoundError("input_file and output_file should be valid files.")

        with open(self.input_file, "r") as input_f, open(output_file, "w") as out_f:
            for line in input_f:
                matched_url = re.findall(final_regex, line)

                if len(matched_url) != 0:
                    matched_url = matched_url[0][1] if self.input_format == "md" else matched_url[0]

                    # This printing step while unnecessary may be useful to make sure things work as expected
                    if verbose:
                        print(f"Found {matched_url}, now validating..")
                    visited_url = urllib.request.urlopen(Request(matched_url, headers={'User-Agent': 'XYZ/3.0'}))
                    url_used = visited_url.geturl()
                    if url_used != matched_url:
                        number_moved += 1
                        if verbose:
                            print(f"{matched_url} replaced with {url_used} in {out_f.name}")
                    out_f.write(line.replace(matched_url, url_used))

        information = "URLs have changed" if number_moved != 1 else "URL has changed"
        print(f"{number_moved} {information} in {self.input_file}")
        return number_moved


class DirURLFix(object):
    def __init__(self, input_dir):
        """
        
        :param input_dir: Path to input_dir.
        
        """
        self.input_dir = input_dir

    def __replace_by_format(self, input_format):
        """

        :param input_format: Input format of the files. Currently supports md and txt
        :return: File with outdated URLs replaced.

        """

        for input_file in Path(self.input_dir).glob(f'*.{input_format}'):
            if '_output' in str(input_file):
                print(f"File already updated in {input_file}")
                continue  # skip output files
            output_file = str(input_file).replace(f'.{input_format}', f'_output.{input_format}')
            if not os.path.exists(output_file):  # skip file that's already been fixed
                with open(output_file, 'w'):
                    pass  # create an empty output file
                return URLFix(input_file, output_file).replace_urls()

    def replace_urls(self):
        number_moved = []
        if not os.path.exists(self.input_dir):
            raise OSError('Path does not exist!')
        if not os.path.isdir(self.input_dir):
            raise NotADirectoryError('Input path must be a directory!')
        for input_format in ('md', 'txt'):
            number_moved.append(self.__replace_by_format(input_format))

        print('All files have been updated, thank you for using urlfix.')
        return number_moved
