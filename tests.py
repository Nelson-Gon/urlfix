import unittest
from urlfix.urlfix import URLFix
from urlfix.dirurlfix import DirURLFix
import os
import glob

dir_path = os.path.dirname(os.path.abspath(__file__))
dir_path = os.path.join("testfiles")
replacement_file = os.path.join(dir_path,"replacement.txt")
# Use the above to make paths to files, avoid changing directory just for tests.
# ToDo: Create order in test files, add these to testfiles?
# Todo: Avoid manually creating file paths.
use_file = os.path.join(dir_path, "testurls.md")
use_file_txt = os.path.join(dir_path, "testurls.txt")
use_object = URLFix(input_file=use_file, output_file=replacement_file)
use_object_txt = URLFix(input_file=use_file_txt, output_file=replacement_file)
use_object_non_existent = URLFix(input_file=use_file, output_file="not_valid.txt")
not_supported_files = URLFix(input_file=os.path.join(dir_path, "testurls.rst"), output_file=replacement_file)

use_dir_object = DirURLFix(os.path.join(dir_path, "testdir"))
use_dir_non_existent = DirURLFix('non_existent')
use_dir_non_dir = DirURLFix(use_file)
use_files_dir = DirURLFix(os.path.join(dir_path, "testdir"))


class Testurlfix(unittest.TestCase):
    def test_instance_creation(self):
        [self.assertTrue(isinstance(urlfix_object, URLFix)) for urlfix_object in [use_object, use_object_txt]]

        with self.assertRaises(ValueError) as err:
            URLFix(input_file=use_file).replace_urls()
        self.assertEqual(str(err.exception), "Please provide an output file to write to.")

    def test_replace_urls(self):
        # Use known changed URLs doc
        with self.assertRaises(FileNotFoundError) as err:
            use_object_non_existent.replace_urls()
        self.assertEqual(str(err.exception), "input_file and output_file should be valid files.")
        number_moved = use_object.replace_urls(verbose=0)
        # 3 out of 9 links should have moved.
        self.assertEqual(number_moved, 3)
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
        # Check that non-supported formats are skipped and an error raised
        with self.assertRaises(NotImplementedError) as err:
            not_supported_files.replace_urls()
        self.assertEqual(str(err.exception), "File format rst is not yet supported.")

        # Check that if a known URL is provided, it is skipped

        number_moved_list = use_files_dir.replace_urls(
            correct_urls=["https://zenodo.org/badge/DOI/10.5281/zenodo.3891106.svg"],
            verbose=True)
        # Since we have three files, assert that the length returned is 3
        self.assertEqual(len(number_moved_list), 3)

        self.assertEqual(number_moved_list[0], 3)
        # 1 since we provided correct URLs. TODO: Figure out how to run both tests
        # 3 since we match double links if []()[]()
        self.assertEqual(number_moved_list[1], 3)
        self.assertEqual(number_moved_list[2], 2)
        # Check skipping --> check that files are created in the above steps
        use_files_dir.replace_urls()
        # Probably better to warn so text can be tested against?
        # TODO: Automate file detection for unit tests.
        testfiles_path = os.path.join(dir_path, "testdir")
        created_output_files = glob.glob(testfiles_path + "/*_output.*")

        for output_file in created_output_files:
            # Avoid try-except-else, not trivial to test
            # Use this for now
            # if this file exists and test passes, delete it
            self.assertTrue(os.path.isfile(output_file))
            print(f"Removing no longer needed file: {output_file}")
            os.remove(output_file)


if __name__ == "__main__":
    unittest.main()
