import os
import tempfile
import unittest
from pathlib import Path

from pdfghost.utils.path_validator import (
    validate_directory_path,
    validate_existing_directory_path,
    validate_file_path,
)


class TestPathValidator(unittest.TestCase):
    def test_file_existing_regular_file_returns_none(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "file.txt"
            path.write_text("data")
            self.assertIsNone(validate_file_path(path))

    def test_file_pathlib_regular_file_returns_none(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "file.bin"
            path.write_bytes(b"data")
            self.assertIsNone(validate_file_path(Path(path)))

    def test_file_missing_raises_file_not_found(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "missing.txt"
            with self.assertRaises(FileNotFoundError):
                validate_file_path(path)

    def test_file_broken_symlink_raises_file_not_found(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "missing-target"
            link = root / "broken-link"
            link.symlink_to(target)

            with self.assertRaises(FileNotFoundError):
                validate_file_path(link)

    def test_file_existing_directory_raises_is_a_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(IsADirectoryError):
                validate_file_path(temp)

    def test_file_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            validate_file_path(None)

    def test_output_directory_existing_directory_returns_none(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertIsNone(validate_directory_path(temp))

    def test_output_directory_pathlib_existing_returns_none(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertIsNone(validate_directory_path(Path(temp)))

    def test_output_directory_missing_nested_is_created(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "parent" / "child"
            self.assertIsNone(validate_directory_path(path))
            self.assertTrue(path.is_dir())

    def test_output_directory_existing_file_raises_not_a_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "file.txt"
            path.write_text("data")

            with self.assertRaises(NotADirectoryError):
                validate_directory_path(path)

    def test_output_directory_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            validate_directory_path(None)

    def test_existing_directory_existing_returns_none(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertIsNone(validate_existing_directory_path(temp))

    def test_existing_directory_pathlib_existing_returns_none(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertIsNone(validate_existing_directory_path(Path(temp)))

    def test_existing_directory_missing_raises_file_not_found(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "missing"

            with self.assertRaises(FileNotFoundError):
                validate_existing_directory_path(path)

    def test_existing_directory_missing_remains_absent(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "missing"

            with self.assertRaises(FileNotFoundError):
                validate_existing_directory_path(path)

            self.assertFalse(path.exists())

    def test_existing_directory_file_raises_not_a_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "file.txt"
            path.write_text("data")

            with self.assertRaises(NotADirectoryError):
                validate_existing_directory_path(path)

    def test_existing_directory_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            validate_existing_directory_path(None)


if __name__ == "__main__":
    unittest.main()
