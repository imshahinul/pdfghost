# pdfghost/functions/splitter.py
from PyPDF2 import PdfReader, PdfWriter
from ..utils.path_validator import validate_file_path, validate_directory_path

def split_pdf(input_path, output_folder, split_range=None):
    """
    Split a PDF into multiple PDFs.

    :param input_path: Path to the input PDF.
    :param output_folder: Folder to save the split PDFs.
    :param split_range: Tuple (start_page, end_page) to split. If None, splits all pages.
    :raises FileNotFoundError: If the input file does not exist.
    """
