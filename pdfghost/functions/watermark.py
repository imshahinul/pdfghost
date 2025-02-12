# pdfghost/functions/watermark.py
from PyPDF2 import PdfReader, PdfWriter
from ..utils.path_validator import validate_file_path

def add_text_watermark(input_path, output_path, text, pages_to_watermark=None):
    """
    Add a text watermark to all or specific pages of a PDF.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the watermarked PDF.
    :param text: Text to use as the watermark.
    :param pages_to_watermark: List of page indices (0-based) to watermark. If None, watermark all pages.
    :raises FileNotFoundError: If the input file does not exist.
    """


def add_image_watermark(input_path, output_path, image_path, pages_to_watermark=None):
    """
    Add an image watermark to all or specific pages of a PDF.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the watermarked PDF.
    :param image_path: Path to the image file to use as the watermark.
    :param pages_to_watermark: List of page indices (0-based) to watermark. If None, watermark all pages.
    :raises FileNotFoundError: If the input file or image does not exist.
    """


def remove_watermark(input_path, output_path, pages_to_clean=None):
    """
    Remove watermarks from all or specific pages of a PDF.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the cleaned PDF.
    :param pages_to_clean: List of page indices (0-based) to clean. If None, clean all pages.
    :raises FileNotFoundError: If the input file does not exist.
    """
