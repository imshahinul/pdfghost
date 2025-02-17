# tests/test_extract.py
import os
import unittest
from PyPDF2 import PdfWriter
from pdfghost.functions.extract import extract_text, extract_images


class TestExtract(unittest.TestCase):
    def setUp(self):
        # Create a valid PDF file for testing
        self.input_pdf = "test.pdf"
        self.output_txt = "output.txt"
        self.output_csv = "output.csv"
        self.output_folder = "output_images"

        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Page 1
        writer.add_blank_page(width=72, height=72)  # Page 2
        with open(self.input_pdf, "wb") as f:
            writer.write(f)

    def test_extract_text_to_txt(self):
        # Test extracting text to a .txt file
        extract_text(self.input_pdf, self.output_txt, format="txt")
        self.assertTrue(os.path.exists(self.output_txt))

    def test_extract_text_to_csv(self):
        # Test extracting text to a .csv file
        extract_text(self.input_pdf, self.output_csv, format="csv")
        self.assertTrue(os.path.exists(self.output_csv))

    def test_extract_text_with_invalid_format(self):
        # Test extracting text with an invalid format
        with self.assertRaises(ValueError):
            extract_text(self.input_pdf, self.output_txt, format="pdf")

    def test_extract_images(self):
        # Test extracting images from a PDF
        extract_images(self.input_pdf, self.output_folder)
        self.assertTrue(os.path.exists(self.output_folder))

    def tearDown(self):
        # Clean up created files and directories
        for path in [self.input_pdf, self.output_txt, self.output_csv]:
            if os.path.exists(path):
                os.remove(path)
        if os.path.exists(self.output_folder):
            for file in os.listdir(self.output_folder):
                os.remove(os.path.join(self.output_folder, file))
            os.rmdir(self.output_folder)


if __name__ == "__main__":
    unittest.main()
