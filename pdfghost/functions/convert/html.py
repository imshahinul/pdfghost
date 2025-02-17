# pdfghost/functions/convert/html.py
import pdfplumber
from ...utils.path_validator import validate_file_path


def pdf_to_html(input_path: str, output_path: str):
    """
    Convert a PDF file into a structured HTML file.

    :param input_path: Path to the input PDF file.
    :param output_path: Path to save the output HTML file.
    :raises FileNotFoundError: If the input file does not exist.
    """
    validate_file_path(input_path)

    # Extract text and structure from the PDF
    with pdfplumber.open(input_path) as pdf:
        html_content = ""
        for page in pdf.pages:
            html_content += page.extract_text() + "<br>"

    # Save the HTML content to the output file
    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)
