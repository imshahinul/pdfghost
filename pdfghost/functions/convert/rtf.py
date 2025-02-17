# pdfghost/functions/latex_convert.py
import os
import subprocess
from ...utils.path_validator import validate_file_path

def markdown_to_pdf(input_path: str, output_path: str):
    """
    Convert a Markdown file into a PDF.

    :param input_path: Path to the input Markdown file.
    :param output_path: Path to save the output PDF.
    :raises FileNotFoundError: If the input file does not exist.
    :raises RuntimeError: If the conversion process fails.
    """

def latex_to_pdf(input_path: str, output_path: str, timeout=30):
    """
    Convert a LaTeX file into a PDF.

    :param input_path: Path to the input LaTeX file.
    :param output_path: Path to save the output PDF.
    :raises FileNotFoundError: If the input file does not exist.
    :raises RuntimeError: If the conversion process fails.
    """
