# tests/test_page_number.py
import os
import math
import unittest
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase.pdfmetrics import stringWidth
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

    def test_numbers_use_actual_dimensions_center_and_font_size_margins(self):
        writer = PdfWriter()
        writer.add_blank_page(width=300, height=500)
        writer.add_blank_page(width=700, height=200)
        writer.add_metadata({"/Subject": "numbering test"})
        with open(self.input_pdf, "wb") as stream:
            writer.write(stream)

        self.assertIsNone(
            add_page_numbers(self.input_pdf, self.output_pdf, "ToP", 20)
        )

        result = PdfReader(self.output_pdf)
        self.assertEqual(result.metadata.subject, "numbering test")
        self.assertEqual(
            [(float(page.mediabox.width), float(page.mediabox.height)) for page in result.pages],
            [(300.0, 500.0), (700.0, 200.0)],
        )
        for index, page in enumerate(result.pages, 1):
            label = f"Page {index}"
            expected_x = (float(page.mediabox.width) - stringWidth(label, "Helvetica", 20)) / 2
            content = page.get_contents().get_data()
            self.assertIn(f"1 0 0 1 {expected_x:g} {float(page.mediabox.height) - 20:g} Tm".encode(), content)
            self.assertIn(b"/F1 20 Tf", content)
            self.assertEqual(page.extract_text(), label + "\n")

        add_page_numbers(self.input_pdf, self.output_pdf, "bottom", 20)
        for page in PdfReader(self.output_pdf).pages:
            self.assertIn(b" 20 Tm", page.get_contents().get_data())

    def test_position_requires_string_before_destination_mutation(self):
        for position in (None, 1, True, ["top"]):
            with self.subTest(position=position):
                Path(self.output_pdf).write_bytes(b"sentinel")
                with self.assertRaises(TypeError):
                    add_page_numbers(self.input_pdf, self.output_pdf, position)
                self.assertEqual(Path(self.output_pdf).read_bytes(), b"sentinel")

    def test_font_size_requires_positive_finite_non_bool_number(self):
        invalid_cases = [
            (True, TypeError),
            ("12", TypeError),
            (None, TypeError),
            (0, ValueError),
            (-1, ValueError),
            (math.inf, ValueError),
            (-math.inf, ValueError),
            (math.nan, ValueError),
        ]
        for font_size, exception in invalid_cases:
            with self.subTest(font_size=font_size):
                Path(self.output_pdf).write_bytes(b"sentinel")
                with self.assertRaises(exception):
                    add_page_numbers(
                        self.input_pdf, self.output_pdf, font_size=font_size
                    )
                self.assertEqual(Path(self.output_pdf).read_bytes(), b"sentinel")

    def test_invalid_position_precedes_input_pdf_processing(self):
        Path(self.input_pdf).write_bytes(b"not a pdf")
        with self.assertRaises(ValueError):
            add_page_numbers(self.input_pdf, self.output_pdf, "middle")

    def tearDown(self):
        # Clean up created files
        for path in [self.input_pdf, self.output_pdf]:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
