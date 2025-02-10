# pdfghost/functions/rearranger.py
import os
from PyPDF2 import PdfReader, PdfWriter
from .merger import merge_pdfs
from ..utils.path_validator import validate_file_path

def rearrange_pdf(input_path, output_path, page_order):
    """
    Rearrange pages in a PDF according to the specified order.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the rearranged PDF.
    :param page_order: List of page indices (0-based) in the desired order.
    :raises FileNotFoundError: If the input file does not exist.
    :raises IndexError: If any page index in `page_order` is out of range.
    """


def merge_and_rearrange(output_path, page_order, *input_paths):
    """
    Merge multiple PDFs and rearrange their pages according to the specified order.

    :param output_path: Path to save the merged and rearranged PDF.
    :param page_order: List of tuples (input_index, page_index) where:
                      - input_index: Index of the input PDF in `input_paths`.
                      - page_index: Page index (0-based) in the specified input PDF.
    :param input_paths: Paths of the PDFs to merge.
    :raises FileNotFoundError: If any input file does not exist.
    :raises IndexError: If any page index in `page_order` is out of range.
    """
    # Merge the input PDFs into a single temporary PDF
