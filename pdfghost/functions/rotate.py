# pdfghost/functions/rotate.py
from pypdf import PdfReader, PdfWriter
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
    validate_file_path(input_path)
    reader = PdfReader(input_path)
    page_count = len(reader.pages)
    _validate_rotation(rotation)
    pages_to_rotate = _validate_pages_to_rotate(pages_to_rotate, page_count)

    writer = PdfWriter(clone_from=input_path)
    for page_index in pages_to_rotate:
        writer.pages[page_index].rotate(rotation)

    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)


def _validate_rotation(rotation):
    if isinstance(rotation, bool) or not isinstance(rotation, int):
        raise TypeError("rotation must be an integer.")
    if rotation not in (90, 180, 270):
        raise ValueError("rotation must be 90, 180, or 270 degrees.")


def _validate_pages_to_rotate(pages_to_rotate, page_count):
    if pages_to_rotate is None:
        return set(range(page_count))
    if not isinstance(pages_to_rotate, (list, tuple, set, frozenset)):
        raise TypeError(
            "pages_to_rotate must be a list, tuple, set, or frozenset."
        )
    if any(
        isinstance(page, bool) or not isinstance(page, int)
        for page in pages_to_rotate
    ):
        raise TypeError("pages_to_rotate must contain only integers.")
    if any(not 0 <= page < page_count for page in pages_to_rotate):
        raise ValueError(
            f"Page indices must satisfy 0 <= page_index < {page_count}."
        )
    return set(pages_to_rotate)
