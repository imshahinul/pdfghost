# pdfghost/functions/splitter.py
from PyPDF2 import PdfReader, PdfWriter
from ..utils.path_validator import validate_file_path, validate_directory_path

def split_pdf(input_path, output_folder, split_range=None):
    """
    Split a PDF into multiple PDFs.

    :param input_path: Path to the input PDF.
    :param output_folder: Folder to save the split PDFs.
    :param split_range: Tuple (start_page, end_page) to split. If None, splits all pages.
    :raises FileNotFoundError: If the input file does not exist.
    """
    validate_file_path(input_path)
    validate_directory_path(output_folder)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    start_page = split_range[0] if split_range else 0
    end_page = split_range[1] if split_range else len(reader.pages)

    for i in range(start_page, end_page):
        writer.add_page(reader.pages[i])

    output_path = f"{output_folder}/split_{start_page + 1}_to_{end_page}.pdf"
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)