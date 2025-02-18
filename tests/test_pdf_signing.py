# tests/test_pdf_signature.py
import os
import unittest
from PyPDF2 import PdfWriter
from pdfghost.functions.pdf_signature import sign_pdf


class TestPdfSignature(unittest.TestCase):
    def setUp(self):
        # Create a valid PDF file for testing
        self.input_pdf = "test.pdf"
        self.output_pdf = "signed.pdf"
        self.certificate_path = "certificate.pfx"

        # Create a sample PDF
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        with open(self.input_pdf, "wb") as f:
            writer.write(f)

        # Create a dummy certificate file
        with open(self.certificate_path, "wb") as f:
            f.write(b"dummy certificate data")

    def test_sign_pdf(self):
        # Test signing a PDF with a certificate
        sign_pdf(self.input_pdf, self.output_pdf, self.certificate_path)
        self.assertTrue(os.path.exists(self.output_pdf))

    def test_sign_pdf_with_invalid_input(self):
        # Test signing with a non-existent PDF file
        with self.assertRaises(FileNotFoundError):
            sign_pdf("nonexistent.pdf", self.output_pdf, self.certificate_path)

    def test_sign_pdf_with_invalid_certificate(self):
        # Test signing with a non-existent certificate file
        with self.assertRaises(FileNotFoundError):
            sign_pdf(self.input_pdf, self.output_pdf, "nonexistent.pfx")

    def tearDown(self):
        # Clean up created files
        for path in [self.input_pdf, self.output_pdf, self.certificate_path]:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
