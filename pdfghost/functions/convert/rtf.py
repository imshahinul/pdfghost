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
    validate_file_path(input_path)

    # Use pandoc to convert Markdown to PDF
    try:
        subprocess.run(
            ["pandoc", input_path, "-o", output_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to convert Markdown to PDF: {e.stderr.decode()}")

def latex_to_pdf(input_path: str, output_path: str, timeout=30):
    """
    Convert a LaTeX file into a PDF.

    :param input_path: Path to the input LaTeX file.
    :param output_path: Path to save the output PDF.
    :raises FileNotFoundError: If the input file does not exist.
    :raises RuntimeError: If the conversion process fails.
    """
    validate_file_path(input_path)
    try:
        result = subprocess.run(
            ["pdflatex", "-output-directory", os.path.dirname(output_path), input_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            #timeout=timeout  # Timeout in seconds
        )
        print(result.stdout)
        print(result.stderr)
    except subprocess.TimeoutExpired:
        raise RuntimeError("LaTeX to PDF conversion timed out.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to convert LaTeX to PDF: {e.stderr.decode()}")
