# tests/test_page_number.py
import os
import unittest
from PyPDF2 import PdfWriter
from pdfghost.functions.page_number import add_page_numbers


class TestPageNumber(unittest.TestCase):
    def setUp(self):
        # Create a valid PDF file for testing
        self.input_pdf = "test.pdf"
        self.output_pdf = "output.pdf"

        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Page 1
        writer.add_blank_page(width=72, height=72)  # Page 2
        with open(self.input_pdf, "wb") as f:
            writer.write(f)

    def test_add_page_numbers_bottom(self):
        # Test adding page numbers at the bottom
        add_page_numbers(self.input_pdf, self.output_pdf, position="bottom")
        self.assertTrue(os.path.exists(self.output_pdf))

    def test_add_page_numbers_top(self):
        # Test adding page numbers at the top
        add_page_numbers(self.input_pdf, self.output_pdf, position="top")
        self.assertTrue(os.path.exists(self.output_pdf))

    def test_add_page_numbers_with_invalid_position(self):
        # Test adding page numbers with an invalid position
        with self.assertRaises(ValueError):
            add_page_numbers(self.input_pdf, self.output_pdf, position="middle")

    def tearDown(self):
        # Clean up created files
        for path in [self.input_pdf, self.output_pdf]:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
