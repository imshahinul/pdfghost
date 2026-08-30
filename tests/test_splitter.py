# tests/test_splitter.py
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pypdf import PdfReader, PdfWriter

from pdfghost.functions.splitter import split_pdf


class TestSplitter(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.input_path = self.root / "test.pdf"
        self.output_folder = self.root / "output"

        writer = PdfWriter()
        writer.add_metadata({"/Title": "split fixture"})
        for width in (72, 144, 216, 288):
            writer.add_blank_page(width=width, height=72)
        with open(self.input_path, "wb") as f:
            writer.write(f)

    def test_split_pdf(self):
        split_pdf(self.input_path, self.output_folder, split_range=(1, 3))

        output = PdfReader(self.output_folder / "split_2_to_3.pdf")
        self.assertEqual([page.mediabox.width for page in output.pages], [144, 216])
        self.assertEqual(output.metadata.title, "split fixture")

    def test_split_pdf_defaults_to_all_pages(self):
        split_pdf(self.input_path, self.output_folder)

        output = PdfReader(self.output_folder / "split_1_to_4.pdf")
        self.assertEqual(len(output.pages), 4)

    def test_split_pdf_with_invalid_input(self):
        with self.assertRaises(FileNotFoundError):
            split_pdf(self.root / "nonexistent.pdf", self.output_folder)

    def test_split_pdf_rejects_invalid_range_types(self):
        invalid_ranges = ([0, 2], (0,), (0, 2, 3), (False, 2), (0, 2.0), "02")

        for split_range in invalid_ranges:
            with self.subTest(split_range=split_range):
                with self.assertRaises(TypeError):
                    split_pdf(self.input_path, self.output_folder, split_range)

    def test_split_pdf_rejects_invalid_range_bounds_without_mutating_output(self):
        invalid_ranges = ((-1, 2), (0, 0), (3, 2), (0, 5), (4, 4))

        for split_range in invalid_ranges:
            with self.subTest(split_range=split_range):
                output_path = self.output_folder / (
                    f"split_{split_range[0] + 1}_to_{split_range[1]}.pdf"
                )
                self.output_folder.mkdir(exist_ok=True)
                output_path.write_bytes(b"sentinel")

                with self.assertRaises(ValueError):
                    split_pdf(self.input_path, self.output_folder, split_range)

                self.assertEqual(output_path.read_bytes(), b"sentinel")

    def test_invalid_range_does_not_create_output_directory(self):
        with self.assertRaises(ValueError):
            split_pdf(self.input_path, self.output_folder, (0, 5))

        self.assertFalse(self.output_folder.exists())

    def tearDown(self):
        self.temporary_directory.cleanup()


if __name__ == "__main__":
    unittest.main()
