import unittest
from functions.run_python_file import run_python_file


class TestRunPythonFile(unittest.TestCase):
    def test_run_valid_file_no_args(self):
        result = run_python_file("calculator", "main.py", [])
        print("test_run_valid_file_no_args result:\n", result)
        self.assertIn("Calculator App", result)

    def test_run_valid_file_with_expression(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        print("test_run_valid_file_with_expression result:\n", result)
        self.assertIn('"expression": "3 + 5"', result)
        self.assertIn('"result": 8', result)

    def test_calculalor_tests(self):
        result = run_python_file("calculator", "tests.py", [])
        print("test_calculalor_tests result:\n", result)
        self.assertIn("OK", result)

    def test_run_non_existent_file(self):
        with self.assertRaises(ValueError) as cm:
            run_python_file("calculator", "nonexistent.py", [])
        print("test_run_non_existent_file raised:\n", cm.exception)

    def test_run_file_outside_directory(self):
        with self.assertRaises(ValueError) as cm:
            run_python_file("calculator", "../main.py", [])
        print("test_run_file_outside_directory raised:\n", cm.exception)

    def test_wrong_file_type(self):
        with self.assertRaises(ValueError) as cm:
            run_python_file("calculator", "lorem.txt", [])
        print("test_wrong_file_type raised:\n", cm.exception)


if __name__ == "__main__":
    unittest.main()
