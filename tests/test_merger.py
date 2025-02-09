# tests/test_merger.py
import os
import unittest
from PyPDF2 import PdfWriter
from pdfghost.functions.merger import merge_pdfs


class TestMerger(unittest.TestCase):
    def setUp(self):
        # Create valid PDF files for testing
        self.input_paths = ["test1.pdf", "test2.pdf"]
        self.output_path = "merged_output.pdf"

        for path in self.input_paths:
            writer = PdfWriter()
            writer.add_blank_page(width=72, height=72)  # Add a blank page
            with open(path, "wb") as f:
                writer.write(f)

    def test_merge_pdfs(self):
        # Test merging two PDFs
        merge_pdfs(self.output_path, *self.input_paths)
        self.assertTrue(os.path.exists(self.output_path))

    def test_merge_pdfs_with_invalid_input(self):
        # Test merging with a non-existent input file
        with self.assertRaises(FileNotFoundError):
            merge_pdfs(self.output_path, "nonexistent.pdf")

    def tearDown(self):
        # Clean up created files
        for path in self.input_paths:
            if os.path.exists(path):
                os.remove(path)
        if os.path.exists(self.output_path):
            os.remove(self.output_path)


if __name__ == "__main__":
    unittest.main()
