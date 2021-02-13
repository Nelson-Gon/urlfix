import unittest
from urlfix import urlfix
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Working in {}".format(os.getcwd()))


class Testurlfix(unittest.TestCase):
    def test_input_format(self):
        # Check that the RegEx works as expected
        res_txt = urlfix.show_parsed_urls("urls.txt")
        self.assertEqual(len(res_txt), 6)
        # What happens if we have .md format
        res_md = urlfix.show_parsed_urls("testurls.md")
        self.assertEqual(len(res_md), 6)

    def test_visiting(self):
        # Use known changed URLs doc
        number_moved = urlfix.replace_urls("testurls.md", verbose=1)
        self.assertEqual(number_moved, 2)


if __name__ == "__main__":
    unittest.main()


