# tests/test_html_convert.py
import os
import unittest
from pathlib import Path

from reportlab.pdfgen import canvas
from pdfghost.functions.convert.html import pdf_to_html


class TestHtmlConvert(unittest.TestCase):
    def setUp(self):
        # Create a valid PDF file for testing
        self.input_pdf = "test.pdf"
        self.output_html = "output.html"

        pdf = canvas.Canvas(self.input_pdf, pagesize=(300, 300))
        pdf.drawString(20, 250, "<unsafe> & text")
        pdf.drawString(20, 230, "second line")
        pdf.showPage()
        pdf.showPage()
        pdf.save()

    def test_pdf_to_html(self):
        # Test converting a PDF to HTML
        self.assertIsNone(pdf_to_html(self.input_pdf, self.output_html))
        content = Path(self.output_html).read_text()
        self.assertIn("<!DOCTYPE html>", content)
        self.assertIn('<html lang="en">', content)
        self.assertIn('<section data-page="1">', content)
        self.assertIn('<section data-page="2">', content)
        self.assertIn("&lt;unsafe&gt; &amp; text", content)
        self.assertNotIn("<unsafe>", content)
        self.assertIn("second line", content)

    def test_pdf_to_html_failure_does_not_mutate_output(self):
        Path(self.input_pdf).write_bytes(b"not a pdf")
        Path(self.output_html).write_bytes(b"sentinel")
        with self.assertRaises(Exception):
            pdf_to_html(self.input_pdf, self.output_html)
        self.assertEqual(Path(self.output_html).read_bytes(), b"sentinel")

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
