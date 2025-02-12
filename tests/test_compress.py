# tests/test_compress.py
import os
import unittest
from PyPDF2 import PdfWriter
from pdfghost.functions.compress import compress_pdf


class TestCompress(unittest.TestCase):
    def setUp(self):
        # Create a valid PDF file for testing
        self.input_path = "test.pdf"
        self.output_path = "output.pdf"

        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Page 1
        writer.add_blank_page(width=72, height=72)  # Page 2
        with open(self.input_path, "wb") as f:
            writer.write(f)

    def test_compress_pdf(self):
        # Test compressing a PDF
        compress_pdf(self.input_path, self.output_path, power=3)
        self.assertTrue(os.path.exists(self.output_path))

    def test_compress_pdf_with_invalid_input(self):
        # Test compressing with a non-existent input file
        with self.assertRaises(FileNotFoundError):
            compress_pdf("nonexistent.pdf", self.output_path)

    def test_compress_pdf_with_invalid_power(self):
        # Test compressing with an invalid compression power
        with self.assertRaises(ValueError):
            compress_pdf(self.input_path, self.output_path, power=6)

    def tearDown(self):
        # Clean up created files
        if os.path.exists(self.input_path):
            os.remove(self.input_path)
        if os.path.exists(self.output_path):
            os.remove(self.output_path)


if __name__ == "__main__":
    unittest.main()
