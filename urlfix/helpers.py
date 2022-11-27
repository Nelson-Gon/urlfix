import urllib
from requests.exceptions import HTTPError
from urllib.error import URLError
from urllib.request import Request
import logging
from collections.abc import Sequence


def check_url(url_link, correct_urls, input_line, logger, url_tracker, changed_url_tracker, verbose, out_file):
    """_summary_

    :param url_link: Link to check/fix
    :type url_link: str
    :param correct_urls: A list of URLs known to be correct
    :type correct_urls: Sequence
    :param input_line: Line containing the URL to check
    :type  input_line: line
    :param logger: logger object
    :type logger: logging
    :param url_tracker: Number of URLs that have changed
    :type url_tracker: int
    :param changed_url_tracker: Number of URLs that have changed
    :type changed_url_tracker: int
    :param verbose: Controls verbosity at the console
    :type verbose: bool
    :param out_file: Output file name
    :return: None
    """
    url_tracker += 1
    if (not isinstance(correct_urls, Sequence) and not url_link in correct_urls):
        try:
            visited_url = urllib.request.urlopen(Request(url_link,
                                                     headers={'User-Agent': 'XYZ/3.0'}))
            url_used = visited_url.geturl()

        except HTTPError as err:
            # Put HTTPError before URLError to avoid issues with inheritance
            # This may be useful for 4xxs, 3xxs if we get past the URLError
            logger.warning(
                f"{url_link} not updated, got HTTP error code: {err.code}.")
            #warnings.warn(f"{final_link} not updated, got HTTP error code: {err.code}.")
            pass

        except URLError as err:
            logger.warning(f"{url_link} not updated. Reason: {err.reason}")
            #warnings.warn(f"{final_link} not updated. Reason: {err.reason}")
            # Must be a way to skip, for now rewrite it in there
            pass

        else:
            if url_used != url_link:
                changed_url_tracker += 1
                line = input_line.replace(url_link, url_used)
                if verbose:
                    logger.info(
                        f"{url_link} replaced with {url_used} in {out_file.name}")
    else:
        # skip current url if it's in 'correct_urls'
        logger.info(f"{url_link} is already valid.")

                        # # This printing step while unnecessary may be useful to make sure things work as expected
                        # if verbose:
                        #     logger.info(
                        #         f"Found {final_link} in {input_f.name}, now validating.. "
                        #     )



def create_logger(log_filename,
                  log_format="%(asctime)s %(levelname)s %(message)s",
                  log_level=logging.WARNING):
    """_summary_

    :param log_filename: Name of the log file 
    :type log_filename: str 
    :param log_format: Format of the log messages, defaults to "%(asctime)s %(levelname)s %(message)s"
    :type log_format: str, optional
    :param log_level: logging log level, defaults to logging.WARNING
    :type log_level: logging, optional
    """
    logging.basicConfig(
        filename=log_filename,
        format=log_format,
        filemode="w"
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    return logger
