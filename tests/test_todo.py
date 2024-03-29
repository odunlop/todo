import unittest
import sys

sys.path.append('../todo')
import get_todo
sys.path.remove('../todo')

test_files = ["./tests/examples/example.txt"]

class TestToDo(unittest.TestCase):

    def test_find_positive_match(self):
        example_regex = ".test.+"
        example_string = "This is a test string"
        result = get_todo.find_match(example_string, example_regex)
        self.assertTrue(result[0])

    def test_negative_match(self):
        example_regex = ".test.+"
        example_string = "This is a wrong string"
        result = get_todo.find_match(example_string, example_regex)
        self.assertFalse(result[0])
    
    def test_list_files(self):
        files = get_todo.list_all_files("./tests/examples")
        self.assertEqual(files, ["./tests/examples/example.txt"])
    
    def test_get_new_todos(self):
        expected_result = {'./tests/examples/example.txt': 
            {
            'This is a single line comment in CSS': '5', 
            'This is a single line comment in Erlang': '6',
            'This is a single line comment in HTML': '4',
            'This is a single line comment in Haskell': '3',
            'This is a single line comment in Java': '2',
            'This is a single line comment in Python': '1'
            }
        }
        result = get_todo.get_new_todos(test_files)
        self.assertEqual(expected_result, result)
    
    def test_get_lines(self):
        todo = "TO-DO"
        result = get_todo.get_lines(test_files[0])
        expected_result = [
            f'[1] # {todo}: This is a single line comment in Python\n', 
            f'[2] // {todo}: This is a single line comment in Java\n', 
            f'[3] – – {todo}: This is a single line comment in Haskell\n', 
            f'[4] <!-- {todo}: This is a single line comment in HTML -->\n', 
            f'[5] /* {todo}: This is a single line comment in CSS *\n', 
            f'[6] % {todo}: This is a single line comment in Erlang\n'
        ]
        self.assertEqual(expected_result, result)
