# pdfbox/functions/remover.py
from pypdf import PdfReader, PdfWriter
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
    page_count = len(reader.pages)
    pages_to_remove = _validate_pages_to_remove(pages_to_remove, page_count)
    writer = _writer_with_metadata(reader)

    for i in range(page_count):
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
    page_count = len(reader.pages)
    _validate_page_count(num_pages, page_count)
    writer = _writer_with_metadata(reader)

    for i in range(num_pages, page_count):
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
    page_count = len(reader.pages)
    _validate_page_count(num_pages, page_count)
    writer = _writer_with_metadata(reader)

    for i in range(page_count - num_pages):
        writer.add_page(reader.pages[i])

    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)


def _validate_pages_to_remove(pages_to_remove, page_count):
    if not isinstance(pages_to_remove, (list, tuple, set, frozenset)):
        raise TypeError("pages_to_remove must be a list, tuple, set, or frozenset.")

    if any(
        isinstance(page, bool) or not isinstance(page, int)
        for page in pages_to_remove
    ):
        raise TypeError("pages_to_remove must contain only integers.")

    invalid_pages = [page for page in pages_to_remove if not 0 <= page < page_count]
    if invalid_pages:
        raise ValueError(
            f"Page indices must satisfy 0 <= page_index < {page_count}."
        )

    return set(pages_to_remove)


def _validate_page_count(num_pages, page_count):
    if isinstance(num_pages, bool) or not isinstance(num_pages, int):
        raise TypeError("num_pages must be an integer.")

    if not 0 <= num_pages <= page_count:
        raise ValueError(f"num_pages must satisfy 0 <= num_pages <= {page_count}.")


def _writer_with_metadata(reader):
    writer = PdfWriter()
    if reader.metadata:
        writer.add_metadata(reader.metadata)
    return writer
