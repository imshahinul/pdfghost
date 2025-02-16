# tests/test_encryption.py
import os
import unittest
from PyPDF2 import PdfWriter
from pdfghost.functions.encryption import encrypt_pdf, decrypt_pdf


class TestEncryption(unittest.TestCase):
    def setUp(self):
        # Create a valid PDF file for testing
        self.input_pdf = "test.pdf"
        self.encrypted_pdf = "encrypted.pdf"
        self.decrypted_pdf = "decrypted.pdf"
        self.password = "password123"

        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Page 1
        writer.add_blank_page(width=72, height=72)  # Page 2
        with open(self.input_pdf, "wb") as f:
            writer.write(f)

    def test_encrypt_pdf(self):
        # Test encrypting a PDF
        encrypt_pdf(self.input_pdf, self.encrypted_pdf, self.password)
        self.assertTrue(os.path.exists(self.encrypted_pdf))

    def test_decrypt_pdf(self):
        # Test decrypting a PDF
        encrypt_pdf(self.input_pdf, self.encrypted_pdf, self.password)
        decrypt_pdf(self.encrypted_pdf, self.decrypted_pdf, self.password)
        self.assertTrue(os.path.exists(self.decrypted_pdf))

    def test_decrypt_pdf_with_incorrect_password(self):
        # Test decrypting a PDF with an incorrect password
        encrypt_pdf(self.input_pdf, self.encrypted_pdf, self.password)
        with self.assertRaises(ValueError):
            decrypt_pdf(self.encrypted_pdf, self.decrypted_pdf, "wrongpassword")

    def test_decrypt_unencrypted_pdf(self):
        # Test decrypting an unencrypted PDF
        with self.assertRaises(ValueError):
            decrypt_pdf(self.input_pdf, self.decrypted_pdf, self.password)

    def tearDown(self):
        # Clean up created files
        for path in [self.input_pdf, self.encrypted_pdf, self.decrypted_pdf]:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
