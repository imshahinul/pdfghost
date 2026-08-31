# pdfghost/functions/latex_convert.py
import math
import os
import shutil
import subprocess
import tempfile
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
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise TypeError("timeout must be an int or float excluding bool")
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be positive and finite")

    validate_file_path(input_path)
    input_path = os.path.abspath(os.fspath(input_path))
    generated_name = os.path.splitext(os.path.basename(input_path))[0] + ".pdf"

    try:
        with tempfile.TemporaryDirectory() as temporary_directory:
            subprocess.run(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "-output-directory",
                    temporary_directory,
                    input_path,
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
            )
            generated_pdf = os.path.join(temporary_directory, generated_name)
            if not os.path.isfile(generated_pdf):
                raise RuntimeError("LaTeX compiler did not produce a PDF.")

            output_directory = os.path.dirname(os.fspath(output_path)) or "."
            with tempfile.NamedTemporaryFile(
                dir=output_directory, suffix=".pdf", delete=False
            ) as temporary_output:
                temporary_output_path = temporary_output.name
            try:
                shutil.copyfile(generated_pdf, temporary_output_path)
                os.replace(temporary_output_path, output_path)
            finally:
                if os.path.exists(temporary_output_path):
                    os.remove(temporary_output_path)
    except subprocess.TimeoutExpired as error:
        raise RuntimeError("LaTeX to PDF conversion timed out.") from error
    except subprocess.CalledProcessError as e:
        diagnostics = e.stderr.decode(errors="replace") if e.stderr else str(e)
        raise RuntimeError(f"Failed to convert LaTeX to PDF: {diagnostics}") from e
    except FileNotFoundError as error:
        raise RuntimeError("LaTeX compiler 'pdflatex' was not found.") from error
