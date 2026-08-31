# pdfghost/functions/convert/html.py
import html
import os
import tempfile

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

    sections = []
    with pdfplumber.open(input_path) as pdf:
        for page_number, page in enumerate(pdf.pages, 1):
            page_text = html.escape(page.extract_text() or "").replace("\n", "<br>\n")
            sections.append(
                f'<section data-page="{page_number}">{page_text}</section>'
            )

    html_content = (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        "<title>PDF conversion</title>\n</head>\n<body>\n"
        + "\n".join(sections)
        + "\n</body>\n</html>\n"
    )

    output_directory = os.path.dirname(os.fspath(output_path)) or "."
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=output_directory, encoding="utf-8", delete=False
        ) as html_file:
            temporary_path = html_file.name
            html_file.write(html_content)
        os.replace(temporary_path, output_path)
        temporary_path = None
    finally:
        if temporary_path is not None and os.path.exists(temporary_path):
            os.remove(temporary_path)
