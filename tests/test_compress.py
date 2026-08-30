# tests/test_compress.py
import os
import unittest
from unittest.mock import patch
from pypdf import PdfReader, PdfWriter
from pypdf._page import PageObject
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
        compress_pdf(self.input_path, self.output_path, power=3)

        reader = PdfReader(self.output_path)
        self.assertEqual(len(reader.pages), 2)

    def test_compression_power_controls_content_stream_effort(self):
        original = PageObject.compress_content_streams

        for power, expected_level in [(0, None), (1, 1), (2, 3), (3, 5), (4, 7), (5, 9)]:
            calls = []

            def record_level(page, level=-1):
                calls.append(level)
                return original(page, level=level)

            with self.subTest(power=power):
                with patch.object(
                    PageObject, "compress_content_streams", new=record_level
                ):
                    compress_pdf(self.input_path, self.output_path, power=power)

                expected_calls = [] if expected_level is None else [expected_level] * 2
                self.assertEqual(calls, expected_calls)

    def test_compress_pdf_preserves_metadata(self):
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        writer.add_metadata({"/Title": "Compression Fixture", "/Author": "PDF Ghost"})
        with open(self.input_path, "wb") as f:
            writer.write(f)

        compress_pdf(self.input_path, self.output_path, power=5)

        metadata = PdfReader(self.output_path).metadata
        self.assertEqual(metadata.title, "Compression Fixture")
        self.assertEqual(metadata.author, "PDF Ghost")

    def test_compress_pdf_with_invalid_input(self):
        # Test compressing with a non-existent input file
        with self.assertRaises(FileNotFoundError):
            compress_pdf("nonexistent.pdf", self.output_path)

    def test_compress_pdf_with_invalid_power(self):
        sentinel = b"existing output must remain unchanged"

        for power in [-1, 6, 2.5, "3", None, True, False]:
            with self.subTest(power=power):
                with open(self.output_path, "wb") as f:
                    f.write(sentinel)

                with self.assertRaises(ValueError):
                    compress_pdf(self.input_path, self.output_path, power=power)

                with open(self.output_path, "rb") as f:
                    self.assertEqual(f.read(), sentinel)

    def tearDown(self):
        # Clean up created files
        if os.path.exists(self.input_path):
            os.remove(self.input_path)
        if os.path.exists(self.output_path):
            os.remove(self.output_path)


if __name__ == "__main__":
    unittest.main()
