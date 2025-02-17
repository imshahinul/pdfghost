# tests/test_html_convert.py
import os
import unittest
from PyPDF2 import PdfWriter
from pdfghost.functions.convert.html import pdf_to_html


class TestHtmlConvert(unittest.TestCase):
    def setUp(self):
        # Create a valid PDF file for testing
        self.input_pdf = "test.pdf"
        self.output_html = "output.html"

        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Page 1
        writer.add_blank_page(width=72, height=72)  # Page 2
        with open(self.input_pdf, "wb") as f:
            writer.write(f)

    def test_pdf_to_html(self):
        # Test converting a PDF to HTML
        pdf_to_html(self.input_pdf, self.output_html)
        self.assertTrue(os.path.exists(self.output_html))

    def test_pdf_to_html_with_invalid_input(self):
        # Test converting a non-existent PDF to HTML
        with self.assertRaises(FileNotFoundError):
            pdf_to_html("nonexistent.pdf", self.output_html)

    def tearDown(self):
        # Clean up created files
        for path in [self.input_pdf, self.output_html]:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
