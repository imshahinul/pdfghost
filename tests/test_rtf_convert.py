import os
import unittest
from unittest.mock import patch, MagicMock

from pdfghost.functions.convert.rtf import markdown_to_pdf, latex_to_pdf


class TestLatexConvert(unittest.TestCase):
    def setUp(self):
        # Create a valid Markdown file for testing
        self.input_markdown = "test.md"
        self.output_markdown_pdf = "output_markdown.pdf"

        with open(self.input_markdown, "w") as f:
            f.write("# Test Markdown\nThis is a test Markdown file.")

        # Create a valid LaTeX file for testing
        self.input_latex = "test.tex"
        self.output_latex_pdf = "output_latex.pdf"

        with open(self.input_latex, "w") as f:
            f.write(
                r"""
                \documentclass{article}
                \begin{document}
                Test LaTeX
                \end{document}
                """
            )

    @patch("pdfghost.functions.convert.rtf.subprocess.run")
    def test_markdown_to_pdf(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b"Success", stderr=b"")

        # Simulate file creation
        with open(self.output_markdown_pdf, "w") as f:
            f.write("PDF content")

        markdown_to_pdf(self.input_markdown, self.output_markdown_pdf)

        self.assertTrue(os.path.exists(self.output_markdown_pdf))
        mock_run.assert_called_once()

    @patch("pdfghost.functions.convert.rtf.subprocess.run")
    def test_latex_to_pdf(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b"Success", stderr=b"")

        # Simulate file creation
        with open(self.output_latex_pdf, "w") as f:
            f.write("PDF content")

        latex_to_pdf(self.input_latex, self.output_latex_pdf)

        self.assertTrue(os.path.exists(self.output_latex_pdf))
        mock_run.assert_called_once()

    @patch("pdfghost.functions.convert.rtf.subprocess.run")
    def test_markdown_to_pdf_with_invalid_input(self, mock_run):
        mock_run.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            markdown_to_pdf("nonexistent.md", self.output_markdown_pdf)

    @patch("pdfghost.functions.convert.rtf.subprocess.run")
    def test_latex_to_pdf_with_invalid_input(self, mock_run):
        mock_run.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            latex_to_pdf("nonexistent.tex", self.output_latex_pdf)

    def tearDown(self):
        # Clean up created files
        for path in [
            self.input_markdown,
            self.output_markdown_pdf,
            self.input_latex,
            self.output_latex_pdf,
        ]:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
