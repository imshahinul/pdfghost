# tests/test_rotate.py
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pypdf import PdfReader, PdfWriter

from pdfghost.functions.rotate import rotate_pdf


class TestRotate(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.input_path = self.root / "test.pdf"
        self.output_path = self.root / "output.pdf"

        writer = PdfWriter()
        writer.add_metadata({"/Title": "rotation fixture"})
        for width in (72, 144, 216):
            writer.add_blank_page(width=width, height=72)
        with self.input_path.open("wb") as stream:
            writer.write(stream)

    def test_rotate_all_pages(self):
        rotate_pdf(self.input_path, self.output_path, rotation=90)

        self.assert_output([90, 90, 90])

    def test_rotate_specific_pages(self):
        rotate_pdf(self.input_path, self.output_path, 180, [0, 2])

        self.assert_output([180, 0, 180])

    def test_empty_and_duplicate_page_collections(self):
        for pages, rotations in (([], [0, 0, 0]), ([1, 1], [0, 270, 0])):
            with self.subTest(pages=pages):
                rotate_pdf(self.input_path, self.output_path, 270, pages)
                self.assert_output(rotations)

    def test_rotate_with_invalid_input(self):
        with self.assertRaises(FileNotFoundError):
            rotate_pdf(self.root / "nonexistent.pdf", self.output_path, 90)

    def test_rotation_rejects_wrong_types_without_mutating_output(self):
        for rotation in (True, 90.0, "90", None):
            with self.subTest(rotation=rotation):
                self.assert_rejected(TypeError, rotation, None)

    def test_rotation_rejects_unsupported_integer_without_mutating_output(self):
        for rotation in (0, 45, 360, -90):
            with self.subTest(rotation=rotation):
                self.assert_rejected(ValueError, rotation, None)

    def test_pages_reject_invalid_collections_and_member_types(self):
        for pages in (1, "1", (value for value in [1]), [True], [1.0], ["1"]):
            with self.subTest(pages=pages):
                self.assert_rejected(TypeError, 90, pages)

    def test_pages_reject_out_of_range_indices(self):
        for pages in ([-1], [3], [1, -1, 3]):
            with self.subTest(pages=pages):
                self.assert_rejected(ValueError, 90, pages)

    def assert_output(self, expected_rotations):
        output = PdfReader(self.output_path)
        self.assertEqual([page.rotation for page in output.pages], expected_rotations)
        self.assertEqual(output.metadata.title, "rotation fixture")

    def assert_rejected(self, exception, rotation, pages):
        self.output_path.write_bytes(b"sentinel")
        with self.assertRaises(exception):
            rotate_pdf(self.input_path, self.output_path, rotation, pages)
        self.assertEqual(self.output_path.read_bytes(), b"sentinel")

    def tearDown(self):
        self.temporary_directory.cleanup()


if __name__ == "__main__":
    unittest.main()
