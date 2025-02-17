# pdfghost/functions/page_number.py
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
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
    validate_file_path(input_path)

    if position.lower() not in ["top", "bottom"]:
        raise ValueError("Position must be 'top' or 'bottom'.")

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        # Create a PDF with the page number
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", font_size)

        # Calculate the position for the page number
        if position.lower() == "top":
            y = 750  # Near the top of the page
        else:
            y = 50  # Near the bottom of the page

        can.drawString(300, y, f"Page {i + 1}")  # Center the page number
        can.save()

        # Merge the page number with the original page
        packet.seek(0)
        number_pdf = PdfReader(packet)
        number_page = number_pdf.pages[0]
        page.merge_page(number_page)
        writer.add_page(page)

    # Save the PDF with page numbers
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)
