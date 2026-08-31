# tests/test_inserter.py
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pypdf import PdfReader, PdfWriter

from pdfghost.functions.inserter import insert_pages


class TestInserter(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.input_path = self.make_pdf("source.pdf", [100, 200, 300], "source")
        self.insert_a = self.make_pdf("insert-a.pdf", [400, 401], "insert A")
        self.insert_b = self.make_pdf("insert-b.pdf", [500], "insert B")
        self.output_path = self.root / "output.pdf"

    def make_pdf(self, name, widths, title):
        path = self.root / name
        writer = PdfWriter()
        writer.add_metadata({"/Title": title})
        for width in widths:
            writer.add_blank_page(width=width, height=72)
        with path.open("wb") as stream:
            writer.write(stream)
        return path

    def test_insert_pages_routes_positions_and_preserves_equal_position_order(self):
        insert_pages(
            self.input_path,
            self.output_path,
            [(3, self.insert_b), (1, self.insert_a), (1, self.insert_b)],
        )

        self.assert_output([100, 400, 401, 500, 200, 300, 500])

    def test_insert_pages_at_start_and_with_empty_insertions(self):
        insert_pages(self.input_path, self.output_path, [(0, self.insert_b)])
        self.assert_output([500, 100, 200, 300])

        insert_pages(self.input_path, self.output_path, [])
        self.assert_output([100, 200, 300])

    def test_insert_pages_with_invalid_input(self):
        with self.assertRaises(FileNotFoundError):
            insert_pages(self.root / "missing.pdf", self.output_path, [])

    def test_insert_pages_with_invalid_insertion_file_does_not_mutate_output(self):
        self.assert_rejected(
            FileNotFoundError, [(1, self.root / "missing.pdf")]
        )

    def test_insertions_reject_invalid_container_and_entry_shapes(self):
        invalid = (
            None,
            {(1, self.insert_b)},
            ((1, self.insert_b) for _ in [0]),
            [1],
            [(1,)],
            [(1, self.insert_b, "extra")],
        )
        for insertions in invalid:
            with self.subTest(insertions=insertions):
                self.assert_rejected(TypeError, insertions)

    def test_insertions_reject_invalid_position_types(self):
        for position in (True, 1.0, "1", None):
            with self.subTest(position=position):
                self.assert_rejected(TypeError, [(position, self.insert_b)])

    def test_insertions_reject_out_of_range_positions(self):
        for position in (-1, 4, 99):
            with self.subTest(position=position):
                self.assert_rejected(ValueError, [(position, self.insert_b)])

    def assert_output(self, expected_widths):
        output = PdfReader(self.output_path)
        self.assertEqual(
            [int(page.mediabox.width) for page in output.pages], expected_widths
        )
        self.assertEqual(output.metadata.title, "source")

    def assert_rejected(self, exception, insertions):
        self.output_path.write_bytes(b"sentinel")
        with self.assertRaises(exception):
            insert_pages(self.input_path, self.output_path, insertions)
        self.assertEqual(self.output_path.read_bytes(), b"sentinel")

    def tearDown(self):
        self.temporary_directory.cleanup()


if __name__ == "__main__":
    unittest.main()
