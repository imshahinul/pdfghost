# pdfghost/functions/page_number.py
import math

from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from io import BytesIO
from ..utils.path_validator import validate_file_path


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
    if not isinstance(position, str):
        raise TypeError("position must be a string")
    normalized_position = position.lower()
    if normalized_position not in ["top", "bottom"]:
        raise ValueError("Position must be 'top' or 'bottom'.")
    if isinstance(font_size, bool) or not isinstance(font_size, (int, float)):
        raise TypeError("font_size must be an int or float excluding bool")
    if not math.isfinite(font_size) or font_size <= 0:
        raise ValueError("font_size must be positive and finite")

    validate_file_path(input_path)

    reader = PdfReader(input_path)
    writer = PdfWriter(clone_from=reader)

    for i, page in enumerate(writer.pages):
        # Create a PDF with the page number
        packet = BytesIO()
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        can = canvas.Canvas(packet, pagesize=(width, height))
        can.setFont("Helvetica", font_size)

        # Calculate the position for the page number
        if normalized_position == "top":
            y = height - font_size
        else:
            y = font_size

        label = f"Page {i + 1}"
        x = (width - stringWidth(label, "Helvetica", font_size)) / 2
        can.drawString(x, y, label)
        can.save()

        # Merge the page number with the original page
        packet.seek(0)
        number_pdf = PdfReader(packet)
        number_page = number_pdf.pages[0]
        page.merge_page(number_page)

    # Save the PDF with page numbers
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)
