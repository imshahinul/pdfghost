# pdfghost/functions/convert/html.py


def pdf_to_html(input_path: str, output_path: str):
    """
    Convert a PDF file into a structured HTML file.

    :param input_path: Path to the input PDF file.
    :param output_path: Path to save the output HTML file.
    :raises FileNotFoundError: If the input file does not exist.
    """
