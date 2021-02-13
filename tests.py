import unittest
from urlfix import urlfix
import os


dir_path = os.path.dirname(os.path.abspath(__file__))
# Use the above to make paths to files, avoid changing directory just for tests.
use_file = os.path.join(dir_path, "testurls.md")
class Testurlfix(unittest.TestCase):
    def test_show_parsed_urls(self):
        # Check that the RegEx works as expected
        # TODO: Fix tests for non markdown mode
        #res_txt = urlfix.show_parsed_urls("urls.txt")
        #self.assertEqual(len(res_txt), 6)
        # What happens if we have .md format
        res_md = urlfix.show_parsed_urls(use_file)
        self.assertEqual(len(res_md), 3)

    def test_replace_urls(self):
        # Use known changed URLs doc
        with self.assertRaises(FileNotFoundError) as err:
            not_valid = urlfix.replace_urls("not_valid.md")
        self.assertEqual(str(err.exception), "input_file and output_file should be valid files.")
        number_moved = urlfix.replace_urls(use_file, verbose=1)
        self.assertEqual(number_moved, 1)


if __name__ == "__main__":
    unittest.main()


