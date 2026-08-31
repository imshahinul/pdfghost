import os
import math
import subprocess
import unittest
from pathlib import Path
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
        def create_pdf(command, **kwargs):
            output_directory = command[command.index("-output-directory") + 1]
            Path(output_directory, "test.pdf").write_bytes(b"PDF content")
            return MagicMock(stdout=b"Success", stderr=b"")

        mock_run.side_effect = create_pdf
        self.assertIsNone(latex_to_pdf(self.input_latex, self.output_latex_pdf, 12.5))
        self.assertEqual(Path(self.output_latex_pdf).read_bytes(), b"PDF content")
        command = mock_run.call_args.args[0]
        self.assertEqual(command[:3], ["pdflatex", "-interaction=nonstopmode", "-halt-on-error"])
        self.assertEqual(Path(command[-1]), Path(self.input_latex).resolve())
        self.assertEqual(mock_run.call_args.kwargs["timeout"], 12.5)
        self.assertTrue(mock_run.call_args.kwargs["check"])

    @patch("pdfghost.functions.convert.rtf.subprocess.run")
    def test_latex_to_pdf_honors_different_output_basename(self, mock_run):
        self.output_latex_pdf = "different-name.pdf"

        def create_pdf(command, **kwargs):
            Path(command[command.index("-output-directory") + 1], "test.pdf").write_bytes(b"pdf")
            return MagicMock(stdout=b"", stderr=b"")

        mock_run.side_effect = create_pdf
        latex_to_pdf(self.input_latex, self.output_latex_pdf)
        self.assertEqual(Path(self.output_latex_pdf).read_bytes(), b"pdf")

    @patch("pdfghost.functions.convert.rtf.subprocess.run")
    def test_latex_failures_do_not_mutate_destination(self, mock_run):
        failures = [
            subprocess.TimeoutExpired("pdflatex", 1),
            subprocess.CalledProcessError(1, ["pdflatex"], stderr=b"bad latex"),
            FileNotFoundError("pdflatex"),
        ]
        for failure in failures:
            with self.subTest(failure=type(failure).__name__):
                Path(self.output_latex_pdf).write_bytes(b"sentinel")
                mock_run.side_effect = failure
                with self.assertRaises(RuntimeError):
                    latex_to_pdf(self.input_latex, self.output_latex_pdf)
                self.assertEqual(Path(self.output_latex_pdf).read_bytes(), b"sentinel")

    @patch("pdfghost.functions.convert.rtf.subprocess.run")
    def test_missing_compiler_output_does_not_mutate_destination(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b"", stderr=b"")
        Path(self.output_latex_pdf).write_bytes(b"sentinel")
        with self.assertRaises(RuntimeError):
            latex_to_pdf(self.input_latex, self.output_latex_pdf)
        self.assertEqual(Path(self.output_latex_pdf).read_bytes(), b"sentinel")

    @patch("pdfghost.functions.convert.rtf.subprocess.run")
    def test_timeout_validation_precedes_process_and_output(self, mock_run):
        cases = [
            (True, TypeError), (None, TypeError), ("30", TypeError),
            (0, ValueError), (-1, ValueError), (math.inf, ValueError),
            (-math.inf, ValueError), (math.nan, ValueError),
        ]
        for timeout, exception in cases:
            with self.subTest(timeout=timeout):
                Path(self.output_latex_pdf).write_bytes(b"sentinel")
                with self.assertRaises(exception):
                    latex_to_pdf(self.input_latex, self.output_latex_pdf, timeout)
                self.assertEqual(Path(self.output_latex_pdf).read_bytes(), b"sentinel")
        mock_run.assert_not_called()

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
