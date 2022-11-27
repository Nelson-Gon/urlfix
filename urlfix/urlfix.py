from collections.abc import Sequence
import os
import re
import urllib.request
from urllib.request import Request
import tempfile
from urllib.error import URLError, HTTPError
from helpers import check_url, create_logger
from multiprocessing import Pool 

logger = create_logger("urlfix_logs.log")


def file_format(in_file):
    """_summary_

    :param in_file: Path to input file that contains URLs to check/fix.
    :type in_file: Accepts md, txt, or rst.
    :return: URLs found in the file
    :rtype: str
    """
    format_pattern = r".+\.(\w+)"
    matches = re.findall(format_pattern, in_file)
    return matches[0] if len(matches) > 0 else ""


class URLFix(object):
    def __init__(self, input_file, output_file=None):
        """
        :param input_file: Path to input_file
        :param output_file: Path to output_file
        """
        self.input_file = input_file
        self.output_file = output_file
        # automatically detect input file format
        self.input_format = file_format(self.input_file)

    def replace_urls(self, verbose=False, correct_urls=None, inplace=False):
        """
        :param verbose Logical. Should you be notified of what URLs have moved? Defaults to False.
        :param correct_urls. A sequence of urls known to be correct.
        :param inplace. Flag for inplace update operation.
        :return  Replaces outdated URL and writes to the specified file. It also returns the number of URLs that have
        changed. The latter is useful for tests.
        """
        if self.input_format not in ("md", "txt", "rmd", "Rmd", "rst"):
            logger.error(
                f"File format {self.input_format} is not yet supported.")
            raise NotImplementedError(
                f"File format {self.input_format} is not yet supported."
            )
        else:
            pass

        link_text = "[^]]+"
        # Better markdown link matching  taken from https://stackoverflow.com/a/23395483/10323798
        # http:// or https:// followed by anything but a closing paren
        actual_link = r"http[s]?://[^)|^\s|?<=\]]+"
        # Need to find more links if using double bracket Markdown hence define single md []() RegEx.
        single_md = r"\[([^]]+)\]\((http[s]?://[^\s|^\)]+)\)"
        combined_regex = (
            rf"\[({link_text})\]\(({actual_link})\)\]\((http[s].*)\)|({single_md})"
        )
        # Match only links in a text file, do not text that follows.
        # Assumes that links will always be followed by a space.
        final_regex = (
            r"http[s]?://[^\s]+"
            if self.input_format in ["rst", "txt"]
            else combined_regex
        )

        if self.output_file is None:
            if not inplace:
                logger.error("Please provide an output file to write to.")
                raise ValueError("Please provide an output file to write to.")
            else:
                # Get directory name from input file path
                output_file = tempfile.NamedTemporaryFile(
                    dir=os.path.dirname(self.input_file), delete=False, mode="w"
                )

        else:
            # if not all(os.path.exists(x) for x in [self.input_file, self.output_file]):
            for file_ in [self.input_file, self.output_file]:
                if not os.path.exists(file_):
                    logger.error(
                        f"Need both input and output files but {file_} does not exist."
                    )
                    raise FileNotFoundError(
                        f"Need both input and output files but {file_} does not exist."
                    )

            output_file = open(self.output_file, "w")

        number_moved = 0
        number_of_urls = 0

        with open(self.input_file, "r") as input_f, output_file as out_f:

            for line in input_f:
                matched_url = re.findall(final_regex, line)
                # Drop empty strings
                if self.input_format in ["md", "rmd", "Rmd"]:
                    matched_url = [
                        list(str(x) for x in texts_links if x != "")
                        for texts_links in matched_url
                    ]
                    for link_texts in matched_url:
                        if len(link_texts) > 1:
                            link_texts = link_texts[1:]
                            # This is used because for some reason we match links twice if single md []()
                            # This isn't ideal
                            # TODO: Use better Regular Expression that matches the target links at once
                            matched_url = list(
                                filter(lambda x: ("https" or "http")
                                       in x, link_texts)
                            )
                if len(matched_url) == 0:
                    # If no URL found, write this line so it is kept in the output file.
                    out_f.write(line)
                    pass
                else:
                    # TODO: Find a way to use threads here. Might need functools partial 
                    [check_url(x, correct_urls=correct_urls) for x in matched_url]
                    

                    out_f.write(line)

        information = "URLs have changed" if number_moved != 1 else "URL has changed"
        logger.info(
            f"{number_moved} {information} of the {number_of_urls} links found in {self.input_file}"
        )
        # We leave this print message here as it is fairly useful
        print(
            f"{number_moved} {information} of the {number_of_urls} links found in {self.input_file}"
        )
        if inplace:
            os.replace(out_f.name, self.input_file)
            if verbose:
                logger.info(
                    f"Renamed temporary file {output_file} as {self.input_file}"
                )
        return number_moved
