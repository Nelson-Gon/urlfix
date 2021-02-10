import urllib.request
import re


def find_links(input_string):
    """

    :param input_string String to search for markdown like links
    :return  Extracts links from MarkDown code

    """
    matched_urls = re.sub(r"(\[.*\])(\()(.*)(\))", "\\3", input_string)

    return matched_urls


def show_parsed_urls(input_file):
    """

    :param input_file: File whose URLs are to be parsed
    :return: URLs in the target file
    """
    input_file = open(input_file)
    matched_urls = list(filter(None, [re.sub("\n|\!", "", find_links(line)) for line in input_file]))
    input_file.close()
    return matched_urls


# Keep url, replacement as pair and replace downstream?
# Directly replace url in document?

def replace_urls(input_file, output_file="replacement.txt", inplace=False, verbose=False, return_matched=False):
    """

    :param input_file File whose links you need to replace or check.

    :param output_file File to write to.
    :param inplace Logical. Determines if you need to replace URLs inplace. Defaults to False.

    :param verbose Logical. Should you be notified of what URLs have moved? Defaults to False.

    :param return_matched Logical. Useful if you want to test on the matched URLs

    :return  File with links replaced.


    """

    # TODO: Speed up file writing and URL checks, avoid unnecessary loops
    # TODO: Work with several files in a directory

    matched_urls = show_parsed_urls(input_file)
    number_moved = 0
    for index, target_url in enumerate(matched_urls):
        visited = urllib.request.urlopen(target_url)
        url_used = visited.geturl()

        if url_used != target_url:
            if inplace:
                output_file = input_file
            with open(input_file, "r") as input_f, open(output_file, "w") as out_f:
                for line in input_f:
                    if verbose:
                        print(f"{target_url} replaced with {url_used} in {out_f}")
                    out_f.write(line.replace(target_url, url_used))

            matched_urls[index] = url_used
            number_moved += 1
    information = "URLS have changed" if number_moved != 1 else "URL has changed"
    print(f"{number_moved} {information}")
    return matched_urls if not return_matched else matched_urls, number_moved
