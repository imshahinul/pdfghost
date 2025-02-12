# tests/test_watermark.py
import os
import unittest
from PyPDF2 import PdfWriter
from PIL import Image
from pdfghost.functions.watermark import (
    add_text_watermark,
    add_image_watermark,
    remove_watermark,
)


class TestWatermark(unittest.TestCase):
    def setUp(self):
        # Create a valid PDF file for testing
        self.input_path = "test.pdf"
        self.output_path = "output.pdf"
        self.image_path = "watermark.png"

        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Page 1
        writer.add_blank_page(width=72, height=72)  # Page 2
        with open(self.input_path, "wb") as f:
            writer.write(f)

        # Create a valid image for testing
        img = Image.new("RGB", (100, 100), color="red")
        img.save(self.image_path)

    def test_add_text_watermark(self):
        # Test adding a text watermark to all pages
        add_text_watermark(self.input_path, self.output_path, text="Confidential")
        self.assertTrue(os.path.exists(self.output_path))

    def test_add_text_watermark_to_specific_pages(self):
        # Test adding a text watermark to specific pages
        add_text_watermark(self.input_path, self.output_path, text="Confidential", pages_to_watermark=[0])
        self.assertTrue(os.path.exists(self.output_path))

    def test_add_image_watermark(self):
        # Test adding an image watermark to all pages
        add_image_watermark(self.input_path, self.output_path, image_path=self.image_path)
        self.assertTrue(os.path.exists(self.output_path))

    def test_add_image_watermark_to_specific_pages(self):
        # Test adding an image watermark to specific pages
        add_image_watermark(self.input_path, self.output_path, image_path=self.image_path, pages_to_watermark=[1])
        self.assertTrue(os.path.exists(self.output_path))

    def test_remove_watermark(self):
        # Test removing watermarks from all pages
        remove_watermark(self.input_path, self.output_path)
        self.assertTrue(os.path.exists(self.output_path))

    def test_remove_watermark_from_specific_pages(self):
        # Test removing watermarks from specific pages
        remove_watermark(self.input_path, self.output_path, pages_to_clean=[0])
        self.assertTrue(os.path.exists(self.output_path))

    def tearDown(self):
        # Clean up created files
        for path in [self.input_path, self.output_path, self.image_path]:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
