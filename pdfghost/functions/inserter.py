# pdfghost/functions/inserter.py
from PyPDF2 import PdfReader, PdfWriter
from ..utils.path_validator import validate_file_path

def insert_pages(input_path, output_path, insertions):
    """
    Insert pages into a PDF at specified positions.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the modified PDF.
    :param insertions: List of tuples (position, page_path), where:
                      - position: Index at which to insert the page (0-based).
                      - page_path: Path to the PDF file containing the page to insert.
    :raises FileNotFoundError: If the input file or any insertion file does not exist.
    """