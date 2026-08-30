# pdfghost/functions/splitter.py
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from ..utils.path_validator import validate_file_path, validate_directory_path


def split_pdf(input_path, output_folder, split_range=None):
    """
    Write a zero-based, half-open range of PDF pages to a new PDF.

    :param input_path: Path to the input PDF.
    :param output_folder: Folder to save the split PDFs.
    :param split_range: Tuple ``(start_page, end_page)``. If None, selects all pages.
    :raises FileNotFoundError: If the input file does not exist.
    :raises TypeError: If split_range is not a pair of integers.
    :raises ValueError: If split_range does not select one or more existing pages.
    """
    validate_file_path(input_path)

    reader = PdfReader(input_path)
    page_count = len(reader.pages)
    start_page, end_page = _validate_split_range(split_range, page_count)
    validate_directory_path(output_folder)

    writer = PdfWriter()
    if reader.metadata:
        writer.add_metadata(reader.metadata)

    for i in range(start_page, end_page):
        writer.add_page(reader.pages[i])

    output_path = Path(output_folder) / f"split_{start_page + 1}_to_{end_page}.pdf"
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)


def _validate_split_range(split_range, page_count):
    if split_range is None:
        split_range = (0, page_count)

    if not isinstance(split_range, tuple) or len(split_range) != 2:
        raise TypeError("split_range must be a tuple of two integers.")

    start_page, end_page = split_range
    if any(isinstance(page, bool) or not isinstance(page, int) for page in split_range):
        raise TypeError("split_range must be a tuple of two integers.")

    if not 0 <= start_page < end_page <= page_count:
        raise ValueError(
            f"split_range must satisfy 0 <= start_page < end_page <= {page_count}."
        )

    return start_page, end_page
