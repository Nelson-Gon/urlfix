from .urlfix import URLFix
from pathlib import Path
import os


class DirURLFix(object):
    """
    Replace Outdated URLs given a directory of files.
    """

    def __init__(self, input_dir):
        """
        :param input_dir: Path to input_dir.
        """
        self.input_dir = input_dir
        self.use_files = Path(self.input_dir)


    def replace_urls(self, **kwargs):
        if not os.path.exists(self.input_dir):
            raise OSError('Path does not exist!')
        if not os.path.isdir(self.input_dir):
            raise NotADirectoryError('Input path must be a directory!')
        number_moved = []
        for _format in ('md', 'txt'):
            for input_file in self.use_files.glob(f"*.{_format}"):
                input_file = str(input_file)
                if "inplace" in kwargs and kwargs["inplace"]:
                    if "_output" in input_file:
                        continue
                    number_moved.append(URLFix(input_file).replace_urls(**kwargs))
                else:
                    if '_output' in input_file:
                        print(f"File is a fix of another file: {input_file}")
                        continue  # skip output files
                    output_file = input_file.replace(f'.{_format}', f'_output.{_format}')
                    if os.path.exists(output_file):
                        print(f"File already fixed: {input_file}")
                        continue  # skip file that's already been fixed

                    with open(output_file, 'w'):
                        pass  # create an empty output file
                    number_moved.append(URLFix(input_file, output_file).replace_urls(**kwargs))

        print('All files have been updated, thank you for using urlfix.')
        return number_moved
