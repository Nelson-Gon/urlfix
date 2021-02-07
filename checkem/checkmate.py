import urllib.request
import re


def find_links(input_string):
    """

    :param input_string String to search for markdown like links
    :param input_format of the links. Currently supports one of md or txt
    :return  Extracts links from MarkDown code

    """
    matched_urls = re.sub(r"(\!|\[.*\])(\()(.*)(\))", "\\3", input_string)

    return matched_urls




def show_parsed_urls(input_file):

    input_file = open(input_file)
    matched_urls = list(filter(None,[re.sub("\n", "", find_links(line)) for line in input_file]))
    input_file.close()
    return matched_urls




# Keep url, replacement as pair and replace downstream?
# Directly replace url in document?

def visit_urls(input_file, verbose=False, return_matched=False):
    """

    :param input_file File whose links you need to replace or check.

    :param verbose Logical. Should you be notified of what URLs have moved? Defaults to False.

    :param return_matched Logical. Useful if you want to test on the matched URLs

    :return  File with links replaced.


    """
    # TODO: Finalize string replacement in input file.

    matched_urls = show_parsed_urls(input_file)
    number_moved = 0
    for index, target_url in enumerate(matched_urls):
        visited = urllib.request.urlopen(target_url)
        url_used = visited.geturl()

        if url_used != target_url:
            if verbose:
                print(f"{target_url} moved to {url_used}")

            matched_urls[index] = url_used
            number_moved += 1
    information = "URLS have changed" if number_moved != 1 else "URL has changed"
    print(f"{number_moved} {information}")
    return matched_urls if not return_matched else matched_urls, number_moved

