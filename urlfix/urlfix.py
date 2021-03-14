from collections.abc import Sequence
import os
import re
import urllib.request
from urllib.request import Request
import tempfile
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

    def replace_urls(self, verbose=False, correct_urls=None, inplace=False):
        """
        :param verbose Logical. Should you be notified of what URLs have moved? Defaults to False.
        :param correct_urls. A sequence of urls known to be correct.
        :param inplace. Flag for inplace update operation.
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

        number_moved = 0
        number_of_urls = 0

        if not self.output_file and not inplace:
            raise ValueError("Please provide an output file to write to.")
        output_file = self.output_file
        if inplace:
            out_f = tempfile.NamedTemporaryFile(mode='r+', dir = os.getcwd(), delete=False)
            output_file = out_f.name
        else:
            out_f = open(output_file, "w")

        if not all(os.path.isfile(x) for x in [self.input_file, output_file]):
            raise FileNotFoundError("input_file and output_file should be valid files.")

        with open(self.input_file, "r") as input_f, out_f:
            
            for line in input_f:
                matched_url = re.findall(final_regex, line)

                if len(matched_url) != 0:
                    matched_url = matched_url[0][1] if self.input_format == "md" else matched_url[0]
                    number_of_urls += 1

                    # make sure 'correct_urls' parameter is a sequence

                    if isinstance(correct_urls, Sequence) and matched_url in correct_urls:
                        # skip current url if it's in 'correct_urls'
                        print(f'{matched_url} is already valid.')
                        continue

                    # This printing step while unnecessary may be useful to make sure things work as expected
                    if verbose:
                        print(f"Found {matched_url} in {input_f.name}, now validating.. ")
                    visited_url = urllib.request.urlopen(Request(matched_url, headers={'User-Agent': 'XYZ/3.0'}))
                    url_used = visited_url.geturl()
                    if url_used != matched_url:
                        number_moved += 1
                        if verbose:
                            print(f"{matched_url} replaced with {url_used} in {out_f.name}")
                    out_f.write(line.replace(matched_url, url_used))
        if inplace:
            with open(self.input_file, "r+") as input_f, open(output_file,'r') as out_f:
                for line in out_f.read():
                    input_f.write(line)
            os.unlink(output_file)
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
