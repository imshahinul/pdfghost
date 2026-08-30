# pdfghost/functions/rearranger.py
from pypdf import PdfReader, PdfWriter
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
    validate_file_path(input_path)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Validate page_order indices
    for page_index in page_order:
        if page_index < 0 or page_index >= len(reader.pages):
            raise IndexError(f"Page index {page_index} is out of range.")

    # Rearrange pages
    for page_index in page_order:
        writer.add_page(reader.pages[page_index])

    # Save the rearranged PDF
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)

def merge_and_rearrange(output_path, page_order, *input_paths):
    """
    Merge multiple PDFs and rearrange their pages according to the specified order.

    :param output_path: Path to save the merged and rearranged PDF.
    :param page_order: List of tuples (input_index, page_index) where:
                      - input_index: Index of the input PDF in `input_paths`.
                      - page_index: Page index (0-based) in the specified input PDF.
    :param input_paths: Paths of the PDFs to merge.
    :raises FileNotFoundError: If any input file does not exist.
    :raises IndexError: If any input or page index in `page_order` is out of range.
    """
    readers = []
    for input_path in input_paths:
        validate_file_path(input_path)
        readers.append(PdfReader(input_path))

    for input_index, page_index in page_order:
        if input_index < 0 or input_index >= len(readers):
            raise IndexError(f"Input index {input_index} is out of range.")
        if page_index < 0 or page_index >= len(readers[input_index].pages):
            raise IndexError(
                f"Page index {page_index} is out of range for input {input_index}."
            )

    writer = PdfWriter()
    for input_index, page_index in page_order:
        writer.add_page(readers[input_index].pages[page_index])

    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)
