# tests/test_remover.py
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pypdf import PdfReader, PdfWriter

from pdfghost.functions.remover import (
    remove_pages,
    remove_pages_from_start,
    remove_pages_from_end,
)


class TestRemover(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.input_path = self.root / "test.pdf"
        self.output_path = self.root / "output.pdf"

        writer = PdfWriter()
        writer.add_metadata({"/Title": "removal fixture"})
        for width in (72, 144, 216, 288):
            writer.add_blank_page(width=width, height=72)
        with open(self.input_path, "wb") as f:
            writer.write(f)

    def test_remove_pages(self):
        remove_pages(self.input_path, self.output_path, pages_to_remove=[1, 3])

        self.assert_output([72, 216])

    def test_remove_pages_from_start(self):
        remove_pages_from_start(self.input_path, self.output_path, num_pages=2)

        self.assert_output([216, 288])

    def test_remove_pages_from_end(self):
        remove_pages_from_end(self.input_path, self.output_path, num_pages=2)

        self.assert_output([72, 144])

    def test_remove_pages_with_invalid_input(self):
        with self.assertRaises(FileNotFoundError):
            remove_pages(self.root / "nonexistent.pdf", self.output_path, [0])

    def test_remove_pages_accepts_empty_and_duplicate_collections(self):
        for pages, expected_widths in (([], [72, 144, 216, 288]), ([1, 1], [72, 216, 288])):
            with self.subTest(pages=pages):
                remove_pages(self.input_path, self.output_path, pages)
                self.assert_output(expected_widths)

    def test_remove_pages_rejects_invalid_collection_types(self):
        invalid_collections = (None, 1, "1", (value for value in [1]))

        for pages in invalid_collections:
            with self.subTest(pages=pages):
                self.assert_rejected_without_output_mutation(
                    TypeError, remove_pages, self.input_path, self.output_path, pages
                )

    def test_remove_pages_rejects_invalid_index_types(self):
        for pages in ([True], [1.0], ["1"]):
            with self.subTest(pages=pages):
                self.assert_rejected_without_output_mutation(
                    TypeError, remove_pages, self.input_path, self.output_path, pages
                )

    def test_remove_pages_rejects_out_of_range_indices(self):
        for pages in ([-1], [4], [1, -1, 4]):
            with self.subTest(pages=pages):
                self.assert_rejected_without_output_mutation(
                    ValueError, remove_pages, self.input_path, self.output_path, pages
                )

    def test_edge_removers_accept_boundary_counts(self):
        for function in (remove_pages_from_start, remove_pages_from_end):
            with self.subTest(function=function.__name__, num_pages=0):
                function(self.input_path, self.output_path, 0)
                self.assert_output([72, 144, 216, 288])
            with self.subTest(function=function.__name__, num_pages=4):
                function(self.input_path, self.output_path, 4)
                self.assert_output([])

    def test_edge_removers_reject_invalid_count_types(self):
        for function in (remove_pages_from_start, remove_pages_from_end):
            for count in (True, 1.0, "1", None):
                with self.subTest(function=function.__name__, count=count):
                    self.assert_rejected_without_output_mutation(
                        TypeError, function, self.input_path, self.output_path, count
                    )

    def test_edge_removers_reject_invalid_count_bounds(self):
        for function in (remove_pages_from_start, remove_pages_from_end):
            for count in (-1, 5):
                with self.subTest(function=function.__name__, count=count):
                    self.assert_rejected_without_output_mutation(
                        ValueError, function, self.input_path, self.output_path, count
                    )

    def assert_output(self, expected_widths):
        output = PdfReader(self.output_path)
        self.assertEqual(
            [page.mediabox.width for page in output.pages], expected_widths
        )
        self.assertEqual(output.metadata.title, "removal fixture")

    def assert_rejected_without_output_mutation(self, exception, function, *args):
        self.output_path.write_bytes(b"sentinel")
        with self.assertRaises(exception):
            function(*args)
        self.assertEqual(self.output_path.read_bytes(), b"sentinel")

    def tearDown(self):
        self.temporary_directory.cleanup()


if __name__ == "__main__":
    unittest.main()
