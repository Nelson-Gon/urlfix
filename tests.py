import unittest
from urlfix.urlfix import URLFix
from urlfix.dirurlfix import DirURLFix
import os
import glob
from shutil import copytree, rmtree

dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfiles")
replacement_file = os.path.join(dir_path, "replacement.txt")
# Use the above to make paths to files, avoid changing directory just for tests.
# Todo: Avoid manually creating file paths.
use_file = os.path.join(dir_path, "testurls.md")
use_file_txt = os.path.join(dir_path, "testurls.txt")
use_object = URLFix(input_file=use_file, output_file=replacement_file)
use_object_txt = URLFix(input_file=use_file_txt, output_file=replacement_file)
use_object_non_existent = URLFix(input_file=use_file, output_file="not_valid.txt")
# Check that rmd works
use_rmd_file = URLFix(input_file=os.path.join(dir_path, "testrmd.rmd"), output_file=replacement_file)
not_supported_files = URLFix(input_file=os.path.join(dir_path, "unsupported.pdf"), output_file=replacement_file)
rst_files = URLFix(input_file=os.path.join(dir_path, "testurls.rst"), output_file=replacement_file)
use_object_inplace = URLFix(input_file=use_file_txt)

use_dir_object = DirURLFix(os.path.join(dir_path, "testdir"))
use_dir_non_existent = DirURLFix('non_existent')
use_dir_non_dir = DirURLFix(use_file)
use_files_dir = DirURLFix(os.path.join(dir_path, "testdir"))
use_inplace_dir = DirURLFix(os.path.join(dir_path, "testinplace"))


def remove_output_files(dir_used):
    created_output_files = glob.glob(os.path.join(dir_path, dir_used) + "/*_output.*")

    for output_file in created_output_files:
        # Avoid try-except-else, not trivial to test
        # Use this for now
        # if this file exists and test passes, delete it
        if os.path.isfile(output_file):
            print(f"Removing no longer needed file: {output_file}")
            os.remove(output_file)


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
        number_moved = use_object.replace_urls(verbose=False)
        # 3 out of 9 links should have moved.
        self.assertEqual(number_moved, 3)
        number_moved_txt = use_object_txt.replace_urls(verbose=True)
        self.assertEqual(number_moved_txt, 2)
        number_moved_rmd = use_rmd_file.replace_urls(verbose=True)
        self.assertEqual(number_moved_rmd, 2)
        # TODO: Avoid checking similar sites more than once (?)
        number_moved_rst = rst_files.replace_urls(verbose=True)
        self.assertEqual(number_moved_rst, 5)


class TestDirURLFix(unittest.TestCase):
    def test_instance_creation(self):
        self.assertTrue(isinstance(use_dir_object, DirURLFix))
        # Clean test folder of results so tests can be repeated.

    def test_replace_urls(self):
        # Use known changed URLs doc
        with self.assertRaises(OSError) as err:
            use_dir_non_existent.replace_urls()
        self.assertEqual(str(err.exception), "Path does not exist!")
        with self.assertRaises(NotADirectoryError) as err:
            use_dir_non_dir.replace_urls()
        self.assertEqual(str(err.exception), "Input path must be a directory!")
        # Check that non-supported formats are skipped and an error raised
        with self.assertRaises(NotImplementedError) as err:
            not_supported_files.replace_urls()
        self.assertEqual(str(err.exception), "File format pdf is not yet supported.")

        # Check that if a known URL is provided, it is skipped

        number_moved_list = use_files_dir.replace_urls(
            correct_urls=["https://zenodo.org/badge/DOI/10.5281/zenodo.3891106.svg"],
            verbose=True)
        # Since we have three files, assert that the length returned is 3
        self.assertEqual(len(number_moved_list), 3)
        # Check the order in which files are read in Linux

        self.assertEqual(number_moved_list[0], 3)
        # 1 since we provided correct URLs. TODO: Figure out how to run both tests
        # 3 since we match double links if []()[]()
        self.assertEqual(number_moved_list[1], 3)
        self.assertEqual(number_moved_list[2], 2)
        # Check skipping --> check that files are created in the above steps
        use_files_dir.replace_urls()

        remove_output_files("testdir")

    def test_replace_urls_inplace(self):
        number_moved_list = use_inplace_dir.replace_urls(verbose=1, inplace=True)

        self.assertEqual(number_moved_list[0], 3)
        self.assertEqual(number_moved_list[1], 3)
        self.assertEqual(number_moved_list[2], 2)

        # If inplace replacement works, then these should all be zeros
        after_inplace = use_inplace_dir.replace_urls(verbose=1, inplace=True)
        [self.assertEqual(x, 0) for x in after_inplace]
        # If tests pass, restore files in the target directory
        test_files = os.path.join(dir_path, "testdir")
        test_inplace_files = os.path.join(dir_path, "testinplace")
        print("Restoring inplace replacement test files after tests....")
        rmtree(test_inplace_files)
        copytree(test_files, test_inplace_files)

    def test_recursion(self):
        # Make path to recursion tests
        recursive_path = os.path.join(dir_path, "recursive")

        recursive_object = DirURLFix(recursive_path, recursive=False)
        number_moved_list = recursive_object.replace_urls(verbose=1)
        # Since we have two root files, then non-recursive replacements should be of length 2
        self.assertEqual(len(number_moved_list), 2)
        # For the first file, we expect only 3 urls to have moved while for the second we expect 5
        self.assertEqual(number_moved_list[0], 3)
        self.assertEqual(number_moved_list[1], 5)
        remove_output_files("recursive")
        # Next, we set recursion to true
        recursive_recursive_object = DirURLFix(recursive_path, recursive=True)
        number_moved_list_recurse = recursive_recursive_object.replace_urls(verbose=1)
        # The first two values are root files as above
        # The second list contains recursive replacements
        self.assertEqual(len(number_moved_list_recurse), 3)
        # 3 because we have three files in the directory recursive/testdir
        self.assertEqual(len(number_moved_list_recurse[2]), 3)
        # Do not test since we have already tested the same directory before?
        # test sub-recursion
        remove_output_files("recursive/testdir")
        remove_output_files("recursive")

    def test_sub_recursion(self):
        print("Testing sub-recursion")
        recursive_path = os.path.join(dir_path, "recursive")
        moved_list = DirURLFix(recursive_path, recursive=True, sub_recursive=True).replace_urls(verbose=1)
        # Assert that we have the expected number of files:
        self.assertEqual(len(moved_list), 3)
        remove_output_files("recursive/testdir/subrecurse")
        remove_output_files("recursive/testdir")


if __name__ == "__main__":
    unittest.main()
