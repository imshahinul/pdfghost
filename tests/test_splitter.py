# tests/test_splitter.py
import os
import unittest
from PyPDF2 import PdfWriter
from pdfghost.functions.splitter import split_pdf

class TestSplitter(unittest.TestCase):
    def setUp(self):
        # Create a valid PDF file for testing
        self.input_path = "test.pdf"
        self.output_folder = "output"

        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Add a blank page
        writer.add_blank_page(width=72, height=72)  # Add another blank page
        with open(self.input_path, "wb") as f:
            writer.write(f)

    def test_split_pdf(self):
        # Test splitting a PDF into a range of pages
        split_pdf(self.input_path, self.output_folder, split_range=(0, 2))
        self.assertTrue(os.path.exists(f"{self.output_folder}/split_1_to_2.pdf"))

    def test_split_pdf_with_invalid_input(self):
        # Test splitting with a non-existent input file
        with self.assertRaises(FileNotFoundError):
            split_pdf("nonexistent.pdf", self.output_folder)

    def test_split_pdf_with_invalid_range(self):
        # Test splitting with an invalid page range
        with self.assertRaises(IndexError):
            split_pdf(self.input_path, self.output_folder, split_range=(10, 20))

    def tearDown(self):
        # Clean up created files and directories
        if os.path.exists(self.input_path):
            os.remove(self.input_path)
        if os.path.exists(self.output_folder):
            for file in os.listdir(self.output_folder):
                os.remove(os.path.join(self.output_folder, file))
            os.rmdir(self.output_folder)

if __name__ == "__main__":
    unittest.main()