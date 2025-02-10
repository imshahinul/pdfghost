# tests/test_rotate.py
import os
import unittest
from PyPDF2 import PdfWriter
from pdfghost.functions.rotate import rotate_pdf


class TestRotate(unittest.TestCase):
    def setUp(self):
        # Create a valid PDF file for testing
        self.input_path = "test.pdf"
        self.output_path = "output.pdf"

        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Page 1
        writer.add_blank_page(width=72, height=72)  # Page 2
        writer.add_blank_page(width=72, height=72)  # Page 3
        with open(self.input_path, "wb") as f:
            writer.write(f)

    def test_rotate_all_pages(self):
        # Test rotating all pages by 90 degrees
        rotate_pdf(self.input_path, self.output_path, rotation=90)
        self.assertTrue(os.path.exists(self.output_path))

    def test_rotate_specific_pages(self):
        # Test rotating specific pages by 180 degrees
        rotate_pdf(self.input_path, self.output_path, rotation=180, pages_to_rotate=[0, 2])
        self.assertTrue(os.path.exists(self.output_path))

    def test_rotate_with_invalid_input(self):
        # Test rotating with a non-existent input file
        with self.assertRaises(FileNotFoundError):
            rotate_pdf("nonexistent.pdf", self.output_path, rotation=90)

    def test_rotate_with_invalid_angle(self):
        # Test rotating with an invalid rotation angle
        with self.assertRaises(ValueError):
            rotate_pdf(self.input_path, self.output_path, rotation=45)

    def tearDown(self):
        # Clean up created files
        if os.path.exists(self.input_path):
            os.remove(self.input_path)
        if os.path.exists(self.output_path):
            os.remove(self.output_path)


if __name__ == "__main__":
    unittest.main()
