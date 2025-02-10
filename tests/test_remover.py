# tests/test_remover.py
import os
import unittest
from PyPDF2 import PdfWriter
from pdfghost.functions.remover import (
    remove_pages,
    remove_pages_from_start,
    remove_pages_from_end,
)


class TestRemover(unittest.TestCase):
    def setUp(self):
        # Create a valid PDF file for testing
        self.input_path = "test.pdf"
        self.output_path = "output.pdf"

        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Add a blank page
        writer.add_blank_page(width=72, height=72)  # Add another blank page
        with open(self.input_path, "wb") as f:
            writer.write(f)

    def test_remove_pages(self):
        # Test removing specific pages
        remove_pages(self.input_path, self.output_path, pages_to_remove=[0, 1])
        self.assertTrue(os.path.exists(self.output_path))

    def test_remove_pages_from_start(self):
        # Test removing pages from the start
        remove_pages_from_start(self.input_path, self.output_path, num_pages=2)
        self.assertTrue(os.path.exists(self.output_path))

    def test_remove_pages_from_end(self):
        # Test removing pages from the end
        remove_pages_from_end(self.input_path, self.output_path, num_pages=2)
        self.assertTrue(os.path.exists(self.output_path))

    def test_remove_pages_with_invalid_input(self):
        # Test removing pages with a non-existent input file
        with self.assertRaises(FileNotFoundError):
            remove_pages("nonexistent.pdf", self.output_path, pages_to_remove=[0])

    def tearDown(self):
        # Clean up created files
        if os.path.exists(self.input_path):
            os.remove(self.input_path)
        if os.path.exists(self.output_path):
            os.remove(self.output_path)


if __name__ == "__main__":
    unittest.main()
