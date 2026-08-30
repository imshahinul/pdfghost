# tests/test_rearranger.py
import os
import unittest
from pypdf import PdfReader, PdfWriter
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
        input_paths = ["test1.pdf", "test2.pdf"]
        page_order = [(1, 0), (0, 1), (1, 1), (0, 0), (1, 0)]

        writer = PdfWriter()
        writer.add_blank_page(width=101, height=201)
        writer.add_blank_page(width=102, height=202)
        with open(input_paths[0], "wb") as f:
            writer.write(f)

        writer = PdfWriter()
        writer.add_blank_page(width=301, height=401)
        writer.add_blank_page(width=302, height=402)
        with open(input_paths[1], "wb") as f:
            writer.write(f)

        try:
            merge_and_rearrange(self.output_path, page_order, *input_paths)

            reader = PdfReader(self.output_path)
            actual_sizes = [
                (float(page.mediabox.width), float(page.mediabox.height))
                for page in reader.pages
            ]
            self.assertEqual(
                actual_sizes,
                [
                    (301.0, 401.0),
                    (102.0, 202.0),
                    (302.0, 402.0),
                    (101.0, 201.0),
                    (301.0, 401.0),
                ],
            )
        finally:
            for path in input_paths:
                if os.path.exists(path):
                    os.remove(path)

    def test_merge_and_rearrange_validates_all_references_before_output_mutation(self):
        input_paths = ["test1.pdf", "test2.pdf"]
        for path, page_count in zip(input_paths, [2, 1]):
            writer = PdfWriter()
            for _ in range(page_count):
                writer.add_blank_page(width=72, height=72)
            with open(path, "wb") as f:
                writer.write(f)

        invalid_orders = [
            [(-1, 0)],
            [(len(input_paths), 0)],
            [(0, -1)],
            [(1, 1)],
            [(0, 0), (1, 1)],
        ]
        sentinel = b"existing output must remain unchanged"

        try:
            for page_order in invalid_orders:
                with self.subTest(page_order=page_order):
                    with open(self.output_path, "wb") as f:
                        f.write(sentinel)

                    with self.assertRaises(IndexError):
                        merge_and_rearrange(
                            self.output_path, page_order, *input_paths
                        )

                    with open(self.output_path, "rb") as f:
                        self.assertEqual(f.read(), sentinel)
        finally:
            for path in input_paths:
                if os.path.exists(path):
                    os.remove(path)

    def test_merge_and_rearrange_leaves_unrelated_temp_file_untouched(self):
        input_path = "test1.pdf"
        temp_path = "temp_merged.pdf"
        sentinel = b"unrelated temporary file"
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        with open(input_path, "wb") as f:
            writer.write(f)
        with open(temp_path, "wb") as f:
            f.write(sentinel)

        try:
            merge_and_rearrange(self.output_path, [(0, 0)], input_path)

            with open(temp_path, "rb") as f:
                self.assertEqual(f.read(), sentinel)
        finally:
            for path in (input_path, temp_path):
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
