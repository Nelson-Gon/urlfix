from .urlfix import URLFix, file_format
import os
import logging 

log_level = logging.DEBUG
log_filename = "dirurlfix_log.log"
log_format = "%(asctime)s %(levelname)s %(message)s"

logging.basicConfig(
    filename= log_filename,
    format = log_format,
    filemode = "w"
    )

logger = logging.getLogger(__name__)

logger.setLevel(log_level)


def replace_urls_root(in_dir, recursive=False, sub_recursive=False, **kwargs):
    """
    :param in_dir:  Input directory
    :param recursive: Bool, should URLs be replaced in sub-directories if they exist?
    :param kwargs: Other arguments to URLFix.replace_urls
    :param sub_recursive: Bool, should URLs be replaced sub-recursively? Defaults to False.
    :return: Files with outdated links validated/replaced, as requested.
    """

    for root, sub_dirs, root_files in os.walk(in_dir):
        number_moved = []  # Hold results
        if root_files:
            # sort root files such that changes are OS independent
            root_files = sorted(root_files)
            for root_file in root_files:
                root_file = os.path.join(in_dir, root_file)
                if file_format(root_file) not in ["md", "txt"]:
                    logger.info(f"{root_file} is of an unsupported file format, skipping...")
                    continue

                if '_output' in root_file:
                    logger.info(f"File {root_file} is a fix of another file")
                    continue  # skip output files
                if "inplace" in kwargs and kwargs["inplace"]:
                    number_moved.append(URLFix(root_file).replace_urls(**kwargs))
                else:
                    output_file = root_file.replace(f'.{file_format(root_file)}',
                                                    f'_output.{file_format(root_file)}')
                    if os.path.exists(output_file):
                        logger.info(f"File already fixed: {root_file}")
                        continue  # skip file that's already been fixed

                    with open(output_file, 'w'):
                        pass  # create an empty output file
                    number_moved.append(URLFix(root_file, output_file).replace_urls(**kwargs))
            if sub_dirs:
                if not recursive:
                    use_grammar = "sub-directory" if len(sub_dirs) == 1 else "sub-directories"
                    logger.warning(f"Found {use_grammar} {','.join(sub_dirs)} but recursion was set to False, exiting..")
                    # This might be useful but maybe user can see what happened in log file instead
                    #warn(f"Found {use_grammar} {','.join(sub_dirs)} but recursion was set to False, exiting..")

                else:
                    for sub_dir in sub_dirs:
                        # Create full paths to sub directories
                        full_sub_dir_path = os.path.join(in_dir, sub_dir)
                        # Add verbosity
                        logger.info(f"Now updating files in {full_sub_dir_path}")
                        # Create new dirurlfix object and recurse
                        # If sub directories, sub-recurse in this sub directory, currently set to one level
                        number_moved.append(replace_urls_root(full_sub_dir_path, recursive=sub_recursive, **kwargs))
        # print('All files have been updated, thank you for using urlfix.')
        # To flatten or not? For now, do not flatten so we know that the second and next are non-root replacements
        return number_moved


class DirURLFix(object):
    """
    Replace Outdated URLs given a directory of files.
    """

    def __init__(self, input_dir, recursive=False, sub_recursive=False):
        """
        :param input_dir: Path to input_dir.
        :param recursive: Should links be replaced in sub directories? defaults to False
        :param sub_recursive: Bool, should URLs be replaced sub-recursively? Defaults to False
        """
        self.input_dir = input_dir
        self.recursive = recursive
        self.sub_recursive = sub_recursive

    def replace_urls(self, **kwargs):
        if not os.path.exists(self.input_dir):
            logger.error("Path does not exist!")
            raise OSError("Path does not exist!")
        if not os.path.isdir(self.input_dir):
            logger.error("Input path must be a directory!")
            raise NotADirectoryError("Input path must be a directory!")

        return replace_urls_root(in_dir=self.input_dir, recursive=self.recursive, sub_recursive=self.sub_recursive,
                                 **kwargs)
