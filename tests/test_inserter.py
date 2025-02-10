# tests/test_inserter.py
import os
import unittest
from PyPDF2 import PdfWriter
from pdfghost.functions.inserter import insert_pages


class TestInserter(unittest.TestCase):
    def setUp(self):
        # Create valid PDF files for testing
        self.input_path = "test.pdf"
        self.output_path = "output.pdf"
        self.insert_page_path = "insert.pdf"

        # Create a valid PDF file for input
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Add a blank page
        with open(self.input_path, "wb") as f:
            writer.write(f)

        # Create a valid PDF file for insertion
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Add a blank page
        with open(self.insert_page_path, "wb") as f:
            writer.write(f)

    def test_insert_pages(self):
        # Test inserting pages at specific positions
        insertions = [
            (1, self.insert_page_path),  # Insert at position 1
            (4, self.insert_page_path),  # Insert at position 4
        ]
        insert_pages(self.input_path, self.output_path, insertions)
        self.assertTrue(os.path.exists(self.output_path))

    def test_insert_pages_with_invalid_input(self):
        # Test inserting pages with a non-existent input file
        insertions = [(1, self.insert_page_path)]
        with self.assertRaises(FileNotFoundError):
            insert_pages("nonexistent.pdf", self.output_path, insertions)

    def test_insert_pages_with_invalid_insertion_file(self):
        # Test inserting pages with a non-existent insertion file
        insertions = [(1, "nonexistent.pdf")]
        with self.assertRaises(FileNotFoundError):
            insert_pages(self.input_path, self.output_path, insertions)

    def tearDown(self):
        # Clean up created files
        for path in [self.input_path, self.output_path, self.insert_page_path]:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
