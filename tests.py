import unittest
from urlfix.urlfix import URLFix
from urlfix.dirurlfix import DirURLFix
import os
import glob
from shutil import copytree, rmtree
import tempfile 

dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfiles")
repl_f = os.path.join(dir_path, "replacement.txt")


def create_test_object(in_f="", kind="file", **kwargs):
    # in_file, out_file = *[os.path.join(dir_path, x) for x in [in_f, out_f]], 
    in_f = os.path.join(dir_path, in_f)
    return URLFix(input_file=in_f, **kwargs) if kind=="file" else DirURLFix(in_f)

def remove_output_files(dir_used=dir_path):
    for output_file in glob.glob(os.path.join(dir_used, "**", "*_output.*")):
        if os.path.isfile(output_file):
            print(f"Removing no longer needed file: {output_file}")
            os.remove(output_file)


class Testurlfix(unittest.TestCase):
    def test_instance_creation(self):
        [self.assertTrue(isinstance(urlfix_object, URLFix)) for urlfix_object in [create_test_object("testurls.md"), create_test_object("testurls.txt")]]

        with self.assertRaises(ValueError) as err:
            create_test_object("testurls.txt").replace_urls()
        self.assertEqual(str(err.exception), "Please provide an output file to write to.")


    def test_replace_urls(self):
        with self.assertRaises(FileNotFoundError) as err:
            create_test_object(in_f="doesnt_exist.txt", output_file=repl_f).replace_urls()
        self.assertEqual(str(err.exception), "input_file and output_file should be valid files.")
        

    def test_md_files(self):    
        md_obj = create_test_object(in_f="testurls.md", output_file = repl_f)
        self.assertEqual(md_obj.replace_urls(verbose=False), 3)

    def test_txt_files(self):
        txt_obj = create_test_object(in_f = "testurls.txt", output_file=repl_f)
        self.assertEqual(txt_obj.replace_urls(verbose=True), 1)

    def test_rmd_files(self):
        rmd_obj = create_test_object(in_f = "testrmd.rmd", output_file=repl_f)
        self.assertEqual(rmd_obj.replace_urls(verbose=True), 1)

    def test_rst_files(self):
        rst_obj = create_test_object(in_f="testurls.rst", output_file= repl_f)
        self.assertEqual(rst_obj.replace_urls(verbose=True), 4) 

    def test_non_support(self):
         # Check that non-supported formats are skipped and an error raised
        with self.assertRaises(NotImplementedError) as err:
            create_test_object("unsupported.pdf", kind="file").replace_urls()
        self.assertEqual(str(err.exception), "File format pdf is not yet supported.")



class TestDirURLFix(unittest.TestCase):
    def test_instance_creation(self):
        self.assertTrue(isinstance(create_test_object("testdir", kind="dir"), DirURLFix))
        # Clean test folder of results so tests can be repeated.

    def test_dir_checks(self):
        # Use known changed URLs doc
        with self.assertRaises(OSError) as err:
            create_test_object("non_existent", kind="dir").replace_urls()
        self.assertEqual(str(err.exception), "Path does not exist!")
        with self.assertRaises(NotADirectoryError) as err:
            create_test_object("testurls.txt", kind="dir").replace_urls()
        self.assertEqual(str(err.exception), "Input path must be a directory!")

    def test_skips(self):
        # Check that if a known URL is provided, it is skipped
        number_moved_list = create_test_object("testdir", kind="dir").replace_urls(
            correct_urls=["https://zenodo.org/badge/DOI/10.5281/zenodo.3891106.svg"],
            verbose=True)
        # # Since we have three files, assert that the length returned is 3
        self.assertEqual(len(number_moved_list), 3)
        self.assertEqual(number_moved_list[0], 3)
        # # 1 since we provided correct URLs. TODO: Figure out how to run both tests
        # # 3 since we match double links if []()[]()
        self.assertEqual(number_moved_list[1], 3)
        self.assertEqual(number_moved_list[2], 1)
        remove_output_files()
    
    def test_inplace_repls(self):
        number_moved_l = create_test_object("testinplace",kind="dir").replace_urls(verbose=1,
                inplace=True)
        self.assertEqual(number_moved_l[0], 3)
        self.assertEqual(number_moved_l[1], 3)
        self.assertEqual(number_moved_l[2], 1)

        # If inplace replacement works, then these should all be zeros
        after_inplace = create_test_object("testinplace",kind="dir").replace_urls(verbose=1, inplace=True)
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
        # For the first file, we expect only 3 urls to have moved while for the second we expect 4
        self.assertEqual(number_moved_list[0], 3)
        self.assertEqual(number_moved_list[1], 4)
        remove_output_files()
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
        remove_output_files()
        

    def test_sub_recursion(self):
        print("Testing sub-recursion")
        recursive_path = os.path.join(dir_path, "recursive")
        moved_list = DirURLFix(recursive_path, recursive=True, sub_recursive=True).replace_urls(verbose=1)
        # Assert that we have the expected number of files:
        self.assertEqual(len(moved_list), 3)
        remove_output_files()
       


if __name__ == "__main__":
    unittest.main()
