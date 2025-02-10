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
    validate_file_path(input_path)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for i in range(len(reader.pages)):
        if i not in pages_to_remove:
            writer.add_page(reader.pages[i])

    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)


def remove_pages_from_start(input_path, output_path, num_pages):
    """
    Remove a specified number of pages from the start of a PDF.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the modified PDF.
    :param num_pages: Number of pages to remove from the start.
    :raises FileNotFoundError: If the input file does not exist.
    """
    validate_file_path(input_path)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for i in range(num_pages, len(reader.pages)):
        writer.add_page(reader.pages[i])

    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)


def remove_pages_from_end(input_path, output_path, num_pages):
    """
    Remove a specified number of pages from the end of a PDF.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the modified PDF.
    :param num_pages: Number of pages to remove from the end.
    :raises FileNotFoundError: If the input file does not exist.
    """
    validate_file_path(input_path)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for i in range(len(reader.pages) - num_pages):
        writer.add_page(reader.pages[i])

    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)
