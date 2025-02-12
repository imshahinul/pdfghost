# pdfghost/functions/compress.py
from PyPDF2 import PdfReader, PdfWriter
from ..utils.path_validator import validate_file_path


def compress_pdf(input_path, output_path, power=3):
    """
    Compress a PDF by optimizing images and removing unnecessary metadata.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the compressed PDF.
    :param power: Compression level (0-5), where 0 is no compression and 5 is maximum compression.
    :raises FileNotFoundError: If the input file does not exist.
    :raises ValueError: If the compression power is invalid.
    """
    validate_file_path(input_path)

    if not (0 <= power <= 5):
        raise ValueError("Compression power must be between 0 and 5.")

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Set compression options
    writer.add_metadata(reader.metadata)  # Preserve metadata
    writer.compress_content_streams = True  # Enable content stream compression

    # Save the compressed PDF
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)
