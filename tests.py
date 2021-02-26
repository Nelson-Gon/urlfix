import unittest
from urlfix.urlfix import *
import os
from pathlib import Path

dir_path = os.path.dirname(os.path.abspath(__file__))
# Use the above to make paths to files, avoid changing directory just for tests.
use_file = os.path.join(dir_path, "testurls.md")
use_file_txt = os.path.join(dir_path, "testurls.txt")

use_object = URLFix(input_file=use_file, output_file="replacement.txt", input_format="md")
use_object_txt = URLFix(input_file=use_file_txt, output_file="replacement.txt", input_format="txt")
use_object_non_existent = URLFix(input_file=use_file, output_file="not_valid.txt")

use_dir_object = DirURLFix(dir_path)
use_dir_non_existent = DirURLFix('non_existent')
use_dir_non_dir = DirURLFix(use_file)


class Testurlfix(unittest.TestCase):
    def test_instance_creation(self):
        self.assertTrue(isinstance(use_object, URLFix))
        self.assertTrue(isinstance(use_object_txt, URLFix))
        with self.assertRaises(ValueError) as err:
            URLFix(input_file=use_file, input_format="md").replace_urls()
        self.assertEqual(str(err.exception), "Please provide an output file to write to.")

    def test_replace_urls(self):
        # Use known changed URLs doc
        with self.assertRaises(FileNotFoundError) as err:
            use_object_non_existent.replace_urls()
        self.assertEqual(str(err.exception), "input_file and output_file should be valid files.")
        number_moved = use_object.replace_urls(verbose=0)
        self.assertEqual(number_moved, 1)
        number_moved_txt = use_object_txt.replace_urls(verbose=1)
        self.assertEqual(number_moved_txt, 2)


class TestDirURLFix(unittest.TestCase):
    def test_instance_creation(self):
        self.assertTrue(isinstance(use_dir_object, DirURLFix))

    def test_replace_urls(self):
        # Use known changed URLs doc
        with self.assertRaises(IOError) as err:
            use_dir_non_existent.replace_urls()
        self.assertEqual(str(err.exception), "Path does not exist!")
        with self.assertRaises(NotADirectoryError) as err:
            use_dir_non_dir.replace_urls()
        self.assertEqual(str(err.exception), "Input path must be a directory!")


if __name__ == "__main__":
    unittest.main()
