# tests/test_pdf_compare.py
import os
import unittest
from PyPDF2 import PdfWriter
from pdfghost.functions.pdf_compare import compare_pdfs


class TestPdfCompare(unittest.TestCase):
    def setUp(self):
        # Create two valid PDF files for testing
        self.file1 = "file1.pdf"
        self.file2 = "file2.pdf"

        # Create file1 with some text
        writer1 = PdfWriter()
        writer1.add_blank_page(width=72, height=72)
        with open(self.file1, "wb") as f:
            writer1.write(f)

        # Create file2 with slightly different text
        writer2 = PdfWriter()
        writer2.add_blank_page(width=72, height=72)
        with open(self.file2, "wb") as f:
            writer2.write(f)

    def test_compare_pdfs_summary(self):
        # Test comparing PDFs with summary output
        result = compare_pdfs(self.file1, self.file2, output_type="summary")
        self.assertIn("Summary of Differences:", result)

    def test_compare_pdfs_side_by_side(self):
        # Test comparing PDFs with side-by-side output
        result = compare_pdfs(self.file1, self.file2, output_type="side_by_side")
        self.assertIn("|", result)  # Check for the separator in side-by-side output

    def test_compare_pdfs_highlight_differences(self):
        # Test comparing PDFs with highlighted differences
        result = compare_pdfs(self.file1, self.file2, output_type="highlight_differences")
        self.assertIn("|", result)  # Check for the separator in highlighted output

    def test_compare_pdfs_version_control(self):
        # Test comparing PDFs with version control output
        result = compare_pdfs(self.file1, self.file2, output_type="version_control")
        self.assertIn("Changes:", result)

    def test_compare_pdfs_annotations(self):
        # Test comparing PDFs with annotations output
        result = compare_pdfs(self.file1, self.file2, output_type="annotations")
        self.assertIn("Annotations:", result)

    def test_compare_pdfs_with_invalid_input(self):
        # Test comparing with a non-existent PDF file
        with self.assertRaises(FileNotFoundError):
            compare_pdfs("nonexistent.pdf", self.file2)

    def tearDown(self):
        # Clean up created files
        for path in [self.file1, self.file2]:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
