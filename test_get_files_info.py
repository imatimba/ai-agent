import unittest
from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def test_current_directory(self):
        result = get_files_info("calculator", ".")
        print("test_current_directory result:\n", result)
        self.assertIn("- tests.py:", result)

    def test_directory(self):
        result = get_files_info("calculator", "pkg")
        print("test_directory result:\n", result)
        self.assertIn("- calculator.py:", result)

    def test_wrong_directory_1(self):
        with self.assertRaises(ValueError) as cm:
            get_files_info("calculator", "../")
        print("test_wrong_directory_1 raised:", cm.exception)

    def test_wrong_directory_2(self):
        with self.assertRaises(ValueError) as cm:
            get_files_info("calculator", "/bin")
        print("test_wrong_directory_2 raised:", cm.exception)


if __name__ == "__main__":
    unittest.main()
