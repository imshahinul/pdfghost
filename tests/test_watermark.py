# tests/test_watermark.py
import os
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader, PdfWriter
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

    def test_text_watermark_uses_each_page_dimensions_and_is_centered(self):
        writer = PdfWriter()
        writer.add_blank_page(width=300, height=500)
        writer.add_blank_page(width=700, height=200)
        writer.add_metadata({"/Title": "dimension test"})
        with open(self.input_path, "wb") as stream:
            writer.write(stream)

        self.assertIsNone(
            add_text_watermark(self.input_path, self.output_path, "CENTER")
        )

        result = PdfReader(self.output_path)
        self.assertEqual(result.metadata.title, "dimension test")
        self.assertEqual(
            [(float(page.mediabox.width), float(page.mediabox.height)) for page in result.pages],
            [(300.0, 500.0), (700.0, 200.0)],
        )
        for page in result.pages:
            self.assertEqual(page.extract_text(), "CENTER\n")
            content = page.get_contents().get_data()
            self.assertIn(b"/F1 60 Tf", content)
            self.assertIn(b"0.5 0.5 0.5 rg", content)
            self.assertIn(b"/gRLs0 gs", content)

    def test_image_watermark_is_centered_at_established_size(self):
        writer = PdfWriter()
        writer.add_blank_page(width=600, height=400)
        with open(self.input_path, "wb") as stream:
            writer.write(stream)

        self.assertIsNone(
            add_image_watermark(self.input_path, self.output_path, self.image_path)
        )

        page = PdfReader(self.output_path).pages[0]
        content = page.get_contents().get_data()
        self.assertIn(b"200 0 0 100 200 150 cm", content)

    def test_page_selection_accepts_frozen_collections_and_is_idempotent(self):
        writer = PdfWriter()
        for _ in range(3):
            writer.add_blank_page(width=300, height=300)
        with open(self.input_path, "wb") as stream:
            writer.write(stream)

        for selection in ([1, 1], (1,), {1}, frozenset({1})):
            with self.subTest(selection=type(selection).__name__):
                add_text_watermark(
                    self.input_path, self.output_path, "MARK", selection
                )
                texts = [page.extract_text() for page in PdfReader(self.output_path).pages]
                self.assertEqual(texts, ["", "MARK\n", ""])

        add_text_watermark(self.input_path, self.output_path, "MARK", [])
        self.assertEqual(
            [page.extract_text() for page in PdfReader(self.output_path).pages],
            ["", "", ""],
        )

    def test_text_and_page_selection_validation_precedes_destination_mutation(self):
        invalid_cases = [
            ((123, None), TypeError),
            (("MARK", 0), TypeError),
            (("MARK", [True]), TypeError),
            (("MARK", [0.0]), TypeError),
            (("MARK", [-1]), ValueError),
            (("MARK", [2]), ValueError),
        ]
        for (text, pages), exception in invalid_cases:
            with self.subTest(text=text, pages=pages):
                Path(self.output_path).write_bytes(b"sentinel")
                with self.assertRaises(exception):
                    add_text_watermark(
                        self.input_path, self.output_path, text, pages
                    )
                self.assertEqual(Path(self.output_path).read_bytes(), b"sentinel")

    def test_image_validation_precedes_pdf_processing_and_destination_mutation(self):
        Path(self.input_path).write_bytes(b"not a pdf")
        Path(self.output_path).write_bytes(b"sentinel")
        with self.assertRaises(FileNotFoundError):
            add_image_watermark(
                self.input_path, self.output_path, "missing-watermark.png"
            )
        self.assertEqual(Path(self.output_path).read_bytes(), b"sentinel")

    def test_image_page_selection_validation_precedes_destination_mutation(self):
        for pages, exception in (("0", TypeError), ([False], TypeError), ([2], ValueError)):
            with self.subTest(pages=pages):
                Path(self.output_path).write_bytes(b"sentinel")
                with self.assertRaises(exception):
                    add_image_watermark(
                        self.input_path, self.output_path, self.image_path, pages
                    )
                self.assertEqual(Path(self.output_path).read_bytes(), b"sentinel")

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
