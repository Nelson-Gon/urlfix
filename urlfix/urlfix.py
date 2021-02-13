import urllib.request
import re
from itertools import chain
from urllib.request import Request
import os


def find_links(input_string, input_format="md"):
    """
    :param input_string String to search for markdown like links
    :param input_format: One of md or txt for now.
    :return:  Extracts links from MarkDown code
    """

    # Better markdown link matching  taken from https://stackoverflow.com/a/23395483/10323798

    link_text = "[^]]+"
    # http:// or https:// followed by anything but a closing paren
    actual_link = "http[s]?://[^)]+"
    # TODO: Include non markdown match in combined_regex
    combined_regex = f"\[({link_text})]\(\s*({actual_link})\s*\)"

    combined_regex = "^http[s].*\s$" if input_format == "txt" else combined_regex

    matched_urls = re.findall(combined_regex, input_string)
    # return 1 since actual URLs are at position one

    return [x[1] for x in matched_urls]


def show_parsed_urls(input_file):
    """

    :param input_file: File whose URLs are to be parsed
    :return: URLs in the target file
    """
    # This leads to unnecessary file opening and closure
    # This function is left here for legacy/testing reasons but may be dropped in the future
    input_file = open(input_file)
    matched_urls = [find_links(line) for line in input_file]
    input_file.close()
    return list(chain(*matched_urls))


# Keep url, replacement as pair and replace downstream?
# Directly replace url in document?

def replace_urls(input_file, output_file="replacement.txt", inplace=False, verbose=False):
    """

    :param input_file File whose links you need to replace or check.

    :param output_file File to write to.
    :param inplace Logical. Determines if you need to replace URLs inplace. Defaults to False.

    :param verbose Logical. Should you be notified of what URLs have moved? Defaults to False.


    :return  Replaces outdated URL and writes to the specified file. It also returns the number of URLs that have
    changed. The latter is useful for tests.


    """

    # TODO: Work with several files in a directory

    if not all(os.path.isfile(x) for x in [input_file, output_file]):
        raise FileNotFoundError("input_file and output_file should be valid files.")

    number_moved = 0
    if inplace:
        output_file = input_file
    with open(input_file, "r") as input_f, open(output_file, "w") as out_f:
        for line in input_f:
            matched_url = find_links(line)
            if len(matched_url) != 0:
                matched_url = matched_url[0]  # Matched URLs are in a list, get as strings, str won't work
                visited_url = urllib.request.urlopen(Request(matched_url, headers={'User-Agent': 'XYZ/3.0'}))
                url_used = visited_url.geturl()
                if url_used != matched_url:
                    number_moved += 1
                    if verbose:
                        print(f"{matched_url} replaced with {url_used} in {out_f.name}")
                out_f.write(line.replace(matched_url, url_used))

    information = "URLS have changed" if number_moved != 1 else "URL has changed"
    print(f"{number_moved} {information}")
    return number_moved
