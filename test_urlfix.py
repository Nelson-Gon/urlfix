import pytest 
from urlfix.urlfix import URLFix
from urlfix.dirurlfix import DirURLFix
import os
from shutil import copytree, rmtree
# better recursive glob unlike using glob
# Only limitation is we are unable to figure out if something is null
from pathlib import Path


dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfiles")
repl_f = os.path.join(dir_path, "replacement.txt")

def make_file(f_path):
    return os.path.join(dir_path, f_path)

@pytest.fixture 
def test_object(in_f="", kind="file", **kwargs):
    def usable_test_object(i_file="", out_f = repl_f, kind = "file",  **kwargs):
        return URLFix(input_file=make_file(i_file), output_file = out_f,  **kwargs) if kind=="file" else DirURLFix(make_file(i_file))
    return usable_test_object

def remove_output_files(dir_used=dir_path):
    for out_file in Path(dir_used).rglob("*_output.*"): 
        print(f"Removing no longer needed file: {out_file}")
        os.remove(out_file)

obj_list = ["testurls.md", "testurls.txt"]
@pytest.mark.parametrize("in_file", obj_list)
def test_instance_creation(in_file, obj_list, test_object):
    assert isinstance(in_file, URLFix)

    with pytest.raises(ValueError) as err:
        test_object(i_file = "testurls.txt", out_f = "").replace_urls()
    assert str(err) == "Please provide an output file to write to."


def test_replace_urls(test_object):
    err_msg = f"Need both input and output files but {make_file('doesnt_exist.txt')} does not exist."
    with pytest.raises(FileNotFoundError, match = err_msg):
        test_object(i_file="doesnt_exist.txt").replace_urls()
        

def test_md_files(test_object):    
    assert test_object(i_file = "testurls.md").replace_urls(verbose=False) == 3

def test_txt_files(test_object):
    assert test_object(i_file = "testurls.txt").replace_urls(verbose=True) == 2

def test_rmd_files(test_object):
    rmd_obj = test_object(i_file = "testrmd.rmd")
    assert rmd_obj.replace_urls(verbose=True) == 2

def test_rst_files(test_object):
    rst_obj = test_object(i_file="testurls.rst")
    assert rst_obj.replace_urls(verbose=True) == 5 

def test_non_support(test_object):
    # Check that non-supported formats are skipped and an error raised
    # Using match as asserting on the expected error message seems to fail for whatever reason
    err_msg = "File format pdf is not yet supported"
    with pytest.raises(NotImplementedError, match  = err_msg):
        test_object(i_file = "unsupported.pdf", kind="file").replace_urls()



# Directory based tests 

def test_instance_creation(test_object):
    assert isinstance(test_object(i_file = "testdir", kind="dir"), DirURLFix)
        
def test_dir_checks(test_object):
    # Use known changed URLs doc
    with pytest.raises(OSError) as err:
        test_object(i_file = "non_existent", kind="dir").replace_urls()
        assert str(err) == "Path does not exist!"
    with pytest.raises(NotADirectoryError) as err:
        test_object(i_file = "testurls.txt", kind="dir").replace_urls()
        assert str(err.exception) == "Input path must be a directory!"

def test_skips(test_object):
    # Check that if a known URL is provided, it is skipped
    number_moved_list = test_object(i_file="testdir", kind="dir").replace_urls(
            correct_urls=["https://zenodo.org/badge/DOI/10.5281/zenodo.3891106.svg"],
            verbose=True)
    # # Since we have three files, assert that the length returned is 3
    assert len(number_moved_list) == 3
    assert number_moved_list[0] == 3
    # # 1 since we provided correct URLs. TODO: Figure out how to run both tests
    # # 3 since we match double links if []()[]()
    assert number_moved_list[1] == 3
    assert number_moved_list[2] == 2
    remove_output_files()
    
def test_inplace_repls(test_object):
    number_moved_l = test_object(i_file = "testinplace",kind="dir").replace_urls(verbose=1,
                inplace=True)
    assert number_moved_l[0] == 3
    assert number_moved_l[1] == 3
    assert number_moved_l[2] == 2

    # If inplace replacement works, then these should all be zeros
    after_inplace = test_object(i_file = "testinplace",kind="dir").replace_urls(verbose=1, inplace=True)
    assert all(x == 0 for x in after_inplace)
    # If tests pass, restore files in the target directory
    test_files = os.path.join(dir_path, "testdir")
    test_inplace_files = os.path.join(dir_path, "testinplace")
    print("Restoring inplace replacement test files after tests....")
    rmtree(test_inplace_files)
    copytree(test_files, test_inplace_files)

# TODO: Make it possible to use our fixture for this 
def test_recursion():
    # Make path to recursion tests
    recursive_path = os.path.join(dir_path, "recursive")
    recursive_object = DirURLFix(recursive_path, recursive=False)
    number_moved_list = recursive_object.replace_urls(verbose=1)
    # Since we have two root files, then non-recursive replacements should be of length 2
    assert len(number_moved_list) == 2
    # For the first file, we expect only 3 urls to have moved while for the second we expect 5
    assert number_moved_list[0] == 3
    assert number_moved_list[1] ==  5
    remove_output_files()
    # Next, we set recursion to true
    recursive_recursive_object = DirURLFix(recursive_path, recursive=True)
    number_moved_list_recurse = recursive_recursive_object.replace_urls(verbose=1)
    # The first two values are root files as above
    # The second list contains recursive replacements
    assert len(number_moved_list_recurse) == 3
    # 3 because we have three files in the directory recursive/testdir
    assert len(number_moved_list_recurse[2]) == 3
    # Do not test since we have already tested the same directory before?
    # test sub-recursion
    remove_output_files()
        

def test_sub_recursion(test_object):
    print("Testing sub-recursion")
    recursive_path = os.path.join(dir_path, "recursive")
    moved_list = DirURLFix(recursive_path, recursive=True, sub_recursive=True).replace_urls(verbose=1)
    # Assert that we have the expected number of files:
    assert len(moved_list) == 3
    remove_output_files()
       



