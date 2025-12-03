import unittest
from functions.write_file import write_file


class TestWriteFile(unittest.TestCase):
    def test_write_valid_file_1(self):
        try:
            write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
            print("test_write_valid_file_1 passed")
        except Exception as e:
            self.fail(f"test_write_valid_file_1 failed: {e}")

    def test_write_valid_file_2(self):
        try:
            write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
            print("test_write_valid_file_2 passed")
        except Exception as e:
            self.fail(f"test_write_valid_file_2 failed: {e}")

    def test_write_invalid_file_1(self):
        with self.assertRaises(ValueError) as cm:
            write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print("test_write_invalid_file_1 raised:", cm.exception)


if __name__ == "__main__":
    unittest.main()
