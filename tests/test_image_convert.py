# tests/test_image_convert.py
import os
import unittest
from PyPDF2 import PdfWriter
from PIL import Image
from pdfghost.functions.convert.image import pdf_to_images, images_to_pdf


class TestImageConvert(unittest.TestCase):
    def setUp(self):
        # Create a valid PDF file for testing
        self.input_pdf = "test.pdf"
        self.output_folder = "output_images"
        self.output_pdf = "output.pdf"

        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Page 1
        writer.add_blank_page(width=72, height=72)  # Page 2
        with open(self.input_pdf, "wb") as f:
            writer.write(f)

        # Create valid image files for testing
        self.image_paths = ["image1.png", "image2.png"]
        for path in self.image_paths:
            img = Image.new("RGB", (100, 100), color="red")
            img.save(path)

    def test_pdf_to_images(self):
        # Test converting PDF to images
        pdf_to_images(self.input_pdf, self.output_folder, format="png")
        self.assertTrue(os.path.exists(os.path.join(self.output_folder, "page_1.png")))
        self.assertTrue(os.path.exists(os.path.join(self.output_folder, "page_2.png")))

    def test_pdf_to_images_with_invalid_format(self):
        # Test converting PDF to images with an invalid format
        with self.assertRaises(ValueError):
            pdf_to_images(self.input_pdf, self.output_folder, format="bmp")

    def test_images_to_pdf(self):
        # Test converting images to PDF
        images_to_pdf(self.output_pdf, *self.image_paths)
        self.assertTrue(os.path.exists(self.output_pdf))

    def test_images_to_pdf_with_invalid_input(self):
        # Test converting images to PDF with a non-existent image file
        with self.assertRaises(FileNotFoundError):
            images_to_pdf(self.output_pdf, "nonexistent.png")

    def tearDown(self):
        # Clean up created files and directories
        if os.path.exists(self.input_pdf):
            os.remove(self.input_pdf)
        if os.path.exists(self.output_pdf):
            os.remove(self.output_pdf)
        if os.path.exists(self.output_folder):
            for file in os.listdir(self.output_folder):
                os.remove(os.path.join(self.output_folder, file))
            os.rmdir(self.output_folder)
        for path in self.image_paths:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
