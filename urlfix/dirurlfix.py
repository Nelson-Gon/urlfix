from .urlfix import URLFix, file_format
import os


class DirURLFix(object):
    """
    Replace Outdated URLs given a directory of files.
    """

    def __init__(self, input_dir, recursive=False):
        """
        :param input_dir: Path to input_dir.
        :param recursive: Should links be replaced in sub directories? defaults to False
        """
        self.input_dir = input_dir
        self.recursive = recursive

    def replace_urls(self, **kwargs):
        if not os.path.exists(self.input_dir):
            raise OSError('Path does not exist!')
        if not os.path.isdir(self.input_dir):
            raise NotADirectoryError('Input path must be a directory!')

        for root, sub_dirs, root_files in os.walk(self.input_dir):

            # Create an empty list to hold links that have changed
            number_moved = []
            # TODO: figure out how to handle both root and sub-directory files.
            if root_files and not self.recursive:
                # sort root files such that changes are OS independent
                root_files = sorted(root_files)
                for root_file in root_files:
                    root_file = os.path.join(self.input_dir, root_file)
                    if file_format(root_file) not in ["md", "txt"]:
                        print(f"{root_file} is of an unsupported file format, skipping...")
                        continue
                        # Create full path

                    if '_output' in root_file:
                        print(f"File {root_file} is a fix of another file")
                        continue  # skip output files
                    if "inplace" in kwargs and kwargs["inplace"]:
                        number_moved.append(URLFix(root_file).replace_urls(**kwargs))
                    else:
                        output_file = root_file.replace(f'.{file_format(root_file)}',
                                                        f'_output.{file_format(root_file)}')
                        if os.path.exists(output_file):
                            print(f"File already fixed: {root_file}")
                            continue  # skip file that's already been fixed

                        with open(output_file, 'w'):
                            pass  # create an empty output file
                        number_moved.append(URLFix(root_file, output_file).replace_urls(**kwargs))

            if sub_dirs:
                print(f"Found the following sub-directories {','.join(sub_dirs)} in {self.input_dir}")
                if self.recursive:
                    for sub_dir in sub_dirs:
                        # Create full paths to sub directories
                        full_sub_dir_path = os.path.join(self.input_dir, sub_dir)
                        # Add verbosity
                        print(f"Now updating files in {full_sub_dir_path}")
                        # Create new dirurlfix object and recurse
                        # Do not sub-recurse in this directory
                        number_moved.append(DirURLFix(full_sub_dir_path).replace_urls(**kwargs))

                else:
                    print(f"Found sub-directories {','.join(sub_dirs)} but recursion was set to False")
            print('All files have been updated, thank you for using urlfix.')
            return number_moved
