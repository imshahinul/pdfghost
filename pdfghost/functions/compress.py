# pdfghost/functions/compress.py
from PyPDF2 import PdfReader, PdfWriter
from ..utils.path_validator import validate_file_path


def compress_pdf(input_path, output_path, power=3):
    """
    Compress a PDF by optimizing images and removing unnecessary metadata.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the compressed PDF.
    :param power: Compression level (0-5), where 0 is no compression and 5 is maximum compression.
    :raises FileNotFoundError: If the input file does not exist.
    :raises ValueError: If the compression power is invalid.
    """
