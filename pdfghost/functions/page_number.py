# pdfghost/functions/page_number.py


def add_page_numbers(input_path, output_path, position="bottom", font_size=12):
    """
    Add page numbers to each page of a PDF.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the PDF with page numbers.
    :param position: Position of the page numbers ("top" or "bottom").
    :param font_size: Font size of the page numbers.
    :raises FileNotFoundError: If the input file does not exist.
    :raises ValueError: If the position is invalid.
    """
