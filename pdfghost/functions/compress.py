# pdfghost/functions/compress.py
from pypdf import PdfReader, PdfWriter
from ..utils.path_validator import validate_file_path


def compress_pdf(input_path, output_path, power=3):
    """
    Losslessly compress a PDF's page content streams.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the compressed PDF.
    :param power: Compression effort (0-5). Level 0 leaves content streams as-is;
                  levels 1-5 use increasing lossless compression effort. Images
                  and metadata are preserved. A smaller output is not guaranteed.
    :raises FileNotFoundError: If the input file does not exist.
    :raises ValueError: If the compression power is invalid.
    """
    validate_file_path(input_path)

    if isinstance(power, bool) or not isinstance(power, int) or not (0 <= power <= 5):
        raise ValueError("Compression power must be an integer between 0 and 5.")

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata(reader.metadata)  # Preserve metadata
    if power:
        compression_level = power * 2 - 1
        for page in writer.pages:
            page.compress_content_streams(level=compression_level)

    # Save the compressed PDF
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)
