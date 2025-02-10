# tests/test_rearranger.py
import os
import unittest
from PyPDF2 import PdfWriter
from pdfghost.functions.rearranger import rearrange_pdf, merge_and_rearrange

class TestRearranger(unittest.TestCase):
    def setUp(self):
        # Create a valid PDF file for testing
        self.input_path = "test.pdf"
        self.output_path = "output.pdf"

        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Page 1
        writer.add_blank_page(width=72, height=72)  # Page 2
        writer.add_blank_page(width=72, height=72)  # Page 3
        with open(self.input_path, "wb") as f:
            writer.write(f)

    def test_rearrange_pdf(self):
        # Test rearranging pages
        page_order = [2, 0, 1]  # New order: Page 3, Page 1, Page 2
        rearrange_pdf(self.input_path, self.output_path, page_order)
        self.assertTrue(os.path.exists(self.output_path))

    def test_rearrange_pdf_with_invalid_input(self):
        # Test rearranging with a non-existent input file
        with self.assertRaises(FileNotFoundError):
            rearrange_pdf("nonexistent.pdf", self.output_path, [0, 1])

    def test_rearrange_pdf_with_invalid_page_order(self):
        # Test rearranging with an out-of-range page index
        with self.assertRaises(IndexError):
            rearrange_pdf(self.input_path, self.output_path, [0, 10])

    def test_merge_and_rearrange(self):
        # Test merging and rearranging pages from multiple PDFs
        input_paths = ["test1.pdf", "test2.pdf"]
        page_order = [(0, 0), (1, 0), (0, 1)]  # Page 1 from test1, Page 1 from test2, Page 2 from test1

        # Create test PDFs
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Page 1 of test1
        writer.add_blank_page(width=72, height=72)  # Page 2 of test1
        with open(input_paths[0], "wb") as f:
            writer.write(f)

        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)  # Page 1 of test2
        with open(input_paths[1], "wb") as f:
            writer.write(f)

        # Perform merge and rearrange
        merge_and_rearrange(self.output_path, page_order, *input_paths)
        self.assertTrue(os.path.exists(self.output_path))

        # Clean up test PDFs
        for path in input_paths:
            if os.path.exists(path):
                os.remove(path)

    def tearDown(self):
        # Clean up created files
        if os.path.exists(self.input_path):
            os.remove(self.input_path)
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

if __name__ == "__main__":
    unittest.main()