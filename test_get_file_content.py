import unittest
from functions.get_file_content import get_file_content


class TestGetFileContent(unittest.TestCase):
    def test_truncate_file(self):
        result = get_file_content("calculator", "lorem.txt")
        print("test_truncate_file result:\n Truncated content")
        self.assertIn('[...File "lorem.txt" truncated at', result)

    def test_main(self):
        result = get_file_content("calculator", "main.py")
        print("test_main result:\n", result)
        self.assertIn("def main():", result)

    def test_calculator(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        print("test_calculator result:\n", result)
        self.assertIn("class Calculator:", result)

    def test_wrong_dir(self):
        with self.assertRaises(ValueError) as cm:
            get_file_content("calculator", "/bin/cat")
        print("test_wrong_dir raised:", cm.exception)

    def test_not_existent_file(self):
        with self.assertRaises(ValueError) as cm:
            get_file_content("calculator", "pkg/does_not_exist.py")
        print("test_not_existent_file raised:", cm.exception)


if __name__ == "__main__":
    unittest.main()
