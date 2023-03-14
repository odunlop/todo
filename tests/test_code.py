from cgi import test
import unittest
import sys
import os

sys.path.append('../todo')
import code_docs
sys.path.remove('../todo')

class TestCode(unittest.TestCase):

    test_template_file = "./tests/examples/README.md.gotmpl"
    test_readme = "./tests/examples/README.md"

# Testing find_match()
    def test_find_positive_match(self):
        example_regex = ".test.+"
        example_string = "This is a test string"
        result = code_docs.find_match(example_string, example_regex)
        self.assertTrue(result[0])
    
    def test_negative_match(self):
        example_regex = ".test.+"
        example_string = "This is a wrong string"
        result = code_docs.find_match(example_string, example_regex)
        self.assertFalse(result[0])

# Testing find_overwrite_section()
    def test_find_files(self):
        lines = ["{{ Documentation Section: ./examples/test.txt }}"]
        filepath = code_docs.find_overwrite_section(lines)
        self.assertEqual(filepath, ["./examples/test.txt"])

# Testing get_lines()
    def test_get_lines_from_file(self):
        filepath = "./tests/examples/test.txt"
        result = code_docs.get_lines(filepath)
        print(result )
        self.assertEqual(
            result, 
            ["Lorem ipsum\n", "\n", "##- Test line\n", "\n", "Lorem ipsum\n", "\n", "##- Second test line\n"]
        )

    def test_error_raised(self):
        filepath = "./wrong/file.txt"
        with self.assertRaises(OSError) as context:
            code_docs.get_lines(filepath)
        self.assertTrue("Invalid filepath provided" in str(context.exception))

# Testing check_files() and check_comments()
    def test_get_comments(self):
        file = ["./tests/examples/test.txt"]
        comments = code_docs.check_files(file)
        self.assertEqual(
            comments, 
            {"./tests/examples/test.txt": ["1. Test line", "2. Second test line"]}
        )

# Testing duplicate_data():
    def check_files_match(self):
        code_docs.duplicate_data(self.test_template_file, self.test_readme)
        template_file_lines = code_docs.get_lines(self.test_template_file)
        readme_lines = code_docs.get_lines(self.test_readme)

        self.assertEqual(template_file_lines, readme_lines)

    def test_readme_exists(self):
        if (os.path.exists(self.test_readme) == False):
            with open(self.test_readme, "a"):
                os.utime(self.test_readme, None)
        self.check_files_match()
    
    def test_readme_not_exist(self):
        if (os.path.exists(self.test_readme) == True):
            os.remove(self.test_readme)
        self.check_files_match()

# Testing format_comments()
    def test_format_comments(self):
        test_comments = ["1. Test line", "2. Second test line"]
        result = code_docs.format_comments(test_comments)
        self.assertEqual(result, "1. Test line\n2. Second test line")
