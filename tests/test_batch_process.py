import os
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfWriter

from pdfghost.functions.batch_process import batch_process
from pdfghost.functions.rotate import rotate_pdf


class TestBatchProcess(unittest.TestCase):
    def setUp(self):
        # Create a folder with sample PDFs for testing
        self.input_folder = "input_pdfs"
        self.output_folder = "output_pdfs"
        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)

        # Create sample PDFs
        self.pdf_files = ["file1.pdf", "file2.pdf"]
        for pdf_file in self.pdf_files:
            writer = PdfWriter()
            writer.add_blank_page(width=72, height=72)
            with open(os.path.join(self.input_folder, pdf_file), "wb") as f:
                writer.write(f)

    def test_batch_rotate(self):
        batch_process(
            self.input_folder,
            self.output_folder,
            rotate_pdf,
            rotation=90,
        )

        for pdf_file in self.pdf_files:
            output_path = os.path.join(self.output_folder, pdf_file)
            self.assertTrue(os.path.exists(output_path))

    def test_batch_process_with_invalid_input_folder(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            missing_input = root / "missing-input"
            missing_output = root / "missing-output"

            with self.assertRaises(FileNotFoundError):
                batch_process(
                    missing_input,
                    missing_output,
                    rotate_pdf,
                    rotation=90,
                )

            self.assertFalse(missing_input.exists())
            self.assertFalse(missing_output.exists())

    def test_batch_process_creates_missing_output_folder(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_folder = root / "input"
            output_folder = root / "output"
            input_folder.mkdir()

            input_pdf = input_folder / "file.pdf"
            writer = PdfWriter()
            writer.add_blank_page(width=72, height=72)

            with input_pdf.open("wb") as output:
                writer.write(output)

            batch_process(
                input_folder,
                output_folder,
                rotate_pdf,
                rotation=90,
            )

            self.assertTrue(output_folder.is_dir())
            self.assertTrue((output_folder / "file.pdf").is_file())

    def test_batch_process_with_no_pdfs(self):
        empty_folder = "empty_folder"
        os.makedirs(empty_folder, exist_ok=True)

        with self.assertRaises(FileNotFoundError):
            batch_process(
                empty_folder,
                self.output_folder,
                rotate_pdf,
                rotation=90,
            )

        os.rmdir(empty_folder)

    def tearDown(self):
        for pdf_file in self.pdf_files:
            input_path = os.path.join(self.input_folder, pdf_file)
            output_path = os.path.join(self.output_folder, pdf_file)

            if os.path.exists(input_path):
                os.remove(input_path)

            if os.path.exists(output_path):
                os.remove(output_path)

        if os.path.exists(self.input_folder):
            os.rmdir(self.input_folder)

        if os.path.exists(self.output_folder):
            os.rmdir(self.output_folder)


if __name__ == "__main__":
    unittest.main()
