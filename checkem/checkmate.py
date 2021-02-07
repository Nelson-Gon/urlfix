import urllib.request
import re


def find_links(input_string):
    """


    :param input_string String to search for markdown like links
    :return  Extracts links from MarkDown code


    """
    matched_urls = re.sub(r"(\[.*\])(\()(.*)(\))", "\\3", input_string)
    return matched_urls


def clean_url(string, remove_what):
    """


    :param string A string for which a replacement is needed
    :param remove_what The pattern to replace
    :return  Replacements as requested.


    """
    return re.sub(remove_what, "", string)


# Keep url, replacement as pair and replace downstream?
# Directly replace url in document?

def visit_urls(input_file):
    """

    :param input_file File whose links you need to replace or check.

    :return  File with links replaced.


    """
    # TODO: Finalize string replacement in input file.

    input_file = open(input_file, "r")
    matched_urls = [clean_url(find_links(line), "\n") for line in input_file]

    for index, target_url in enumerate(matched_urls):
        visited = urllib.request.urlopen(target_url)
        url_used = visited.geturl()
        if url_used != target_url:
            print(f"{target_url} moved to {url_used}")
            matched_urls[index] = url_used
    return matched_urls
