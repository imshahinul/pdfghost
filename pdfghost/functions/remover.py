# pdfbox/functions/remover.py
from PyPDF2 import PdfReader, PdfWriter
from ..utils.path_validator import validate_file_path


def remove_pages(input_path, output_path, pages_to_remove):
    """
    Remove specific pages from a PDF.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the modified PDF.
    :param pages_to_remove: List of page indices to remove (0-based).
    :raises FileNotFoundError: If the input file does not exist.
    """



def remove_pages_from_start(input_path, output_path, num_pages):
    """
    Remove a specified number of pages from the start of a PDF.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the modified PDF.
    :param num_pages: Number of pages to remove from the start.
    :raises FileNotFoundError: If the input file does not exist.
    """



def remove_pages_from_end(input_path, output_path, num_pages):
    """
    Remove a specified number of pages from the end of a PDF.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the modified PDF.
    :param num_pages: Number of pages to remove from the end.
    :raises FileNotFoundError: If the input file does not exist.
    """
