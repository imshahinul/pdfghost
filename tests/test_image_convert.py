# tests/test_image_convert.py
import os
import unittest
from pathlib import Path

from pypdf import PdfWriter
from pypdf import PdfReader
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

    def test_images_to_pdf_requires_an_image_without_mutating_output(self):
        Path(self.output_pdf).write_bytes(b"sentinel")
        with self.assertRaises(ValueError):
            images_to_pdf(self.output_pdf)
        self.assertEqual(Path(self.output_pdf).read_bytes(), b"sentinel")

    def test_images_to_pdf_validates_all_paths_before_decoding_or_output(self):
        Path(self.image_paths[0]).write_bytes(b"corrupt image")
        Path(self.output_pdf).write_bytes(b"sentinel")
        with self.assertRaises(FileNotFoundError):
            images_to_pdf(self.output_pdf, self.image_paths[0], "missing.png")
        self.assertEqual(Path(self.output_pdf).read_bytes(), b"sentinel")

    def test_images_to_pdf_decoding_failure_does_not_mutate_output(self):
        Path(self.image_paths[0]).write_bytes(b"corrupt image")
        Path(self.output_pdf).write_bytes(b"sentinel")
        with self.assertRaises(Exception):
            images_to_pdf(self.output_pdf, self.image_paths[0])
        self.assertEqual(Path(self.output_pdf).read_bytes(), b"sentinel")

    def test_images_to_pdf_preserves_order_dimensions_and_supports_rgba(self):
        Image.new("RGBA", (40, 20), (255, 0, 0, 100)).save(self.image_paths[0])
        Image.new("L", (30, 50), 128).save(self.image_paths[1])
        self.assertIsNone(images_to_pdf(self.output_pdf, *self.image_paths))
        pages = PdfReader(self.output_pdf).pages
        self.assertEqual(
            [(float(page.mediabox.width), float(page.mediabox.height)) for page in pages],
            [(40.0, 20.0), (30.0, 50.0)],
        )

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
