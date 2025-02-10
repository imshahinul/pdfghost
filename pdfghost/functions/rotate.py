# pdfghost/functions/rotate.py
from PyPDF2 import PdfReader, PdfWriter
from ..utils.path_validator import validate_file_path


def rotate_pdf(input_path, output_path, rotation, pages_to_rotate=None):
    """
    Rotate specific pages or the entire PDF by a given angle.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the rotated PDF.
    :param rotation: Angle to rotate the pages (90, 180, or 270 degrees).
    :param pages_to_rotate: List of page indices (0-based) to rotate. If None, rotate all pages.
    :raises FileNotFoundError: If the input file does not exist.
    :raises ValueError: If the rotation angle is invalid.
    """
