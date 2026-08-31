# pdfghost/functions/inserter.py
from pypdf import PdfReader, PdfWriter
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
    validate_file_path(input_path)
    reader = PdfReader(input_path)
    insertions = _validate_insertions(insertions, len(reader.pages))

    insertion_readers = {}
    for _, page_path in insertions:
        validate_file_path(page_path)
        if page_path not in insertion_readers:
            insertion_readers[page_path] = PdfReader(page_path)

    writer = PdfWriter()
    if reader.metadata:
        writer.add_metadata(reader.metadata)

    insertion_index = 0
    insertions_sorted = sorted(insertions, key=lambda x: x[0])

    for i in range(len(reader.pages)):
        # Insert pages before the current page if needed
        while insertion_index < len(insertions_sorted) and insertions_sorted[insertion_index][0] == i:
            _, page_path = insertions_sorted[insertion_index]
            insertion_reader = insertion_readers[page_path]
            for page in insertion_reader.pages:
                writer.add_page(page)
            insertion_index += 1

        # Add the current page from the original PDF
        writer.add_page(reader.pages[i])

    # Insert any remaining pages at the end
    while insertion_index < len(insertions_sorted):
        _, page_path = insertions_sorted[insertion_index]
        insertion_reader = insertion_readers[page_path]
        for page in insertion_reader.pages:
            writer.add_page(page)
        insertion_index += 1

    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)


def _validate_insertions(insertions, page_count):
    if not isinstance(insertions, (list, tuple)):
        raise TypeError("insertions must be a list or tuple.")

    validated = []
    for insertion in insertions:
        if not isinstance(insertion, (list, tuple)) or len(insertion) != 2:
            raise TypeError(
                "Each insertion must be a two-item list or tuple."
            )
        position, page_path = insertion
        if isinstance(position, bool) or not isinstance(position, int):
            raise TypeError("Insertion positions must be integers.")
        if not 0 <= position <= page_count:
            raise ValueError(
                f"Insertion positions must satisfy 0 <= position <= {page_count}."
            )
        validated.append((position, page_path))

    return validated
