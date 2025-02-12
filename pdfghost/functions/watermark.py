# pdfghost/functions/watermark.py
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from ..utils.path_validator import validate_file_path

def add_text_watermark(input_path, output_path, text, pages_to_watermark=None):
    """
    Add a text watermark to all or specific pages of a PDF.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the watermarked PDF.
    :param text: Text to use as the watermark.
    :param pages_to_watermark: List of page indices (0-based) to watermark. If None, watermark all pages.
    :raises FileNotFoundError: If the input file does not exist.
    """
    validate_file_path(input_path)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Create a watermark PDF
    watermark_pdf = BytesIO()
    c = canvas.Canvas(watermark_pdf, pagesize=letter)
    c.setFont("Helvetica", 60)
    c.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.5)  # Light gray with transparency
    c.drawString(100, 100, text)  # Position the watermark
    c.save()

    # Apply the watermark to the specified pages
    watermark_reader = PdfReader(watermark_pdf)
    watermark_page = watermark_reader.pages[0]

    for i in range(len(reader.pages)):
        page = reader.pages[i]
        if pages_to_watermark is None or i in pages_to_watermark:
            page.merge_page(watermark_page)
        writer.add_page(page)

    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)

def add_image_watermark(input_path, output_path, image_path, pages_to_watermark=None):
    """
    Add an image watermark to all or specific pages of a PDF.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the watermarked PDF.
    :param image_path: Path to the image file to use as the watermark.
    :param pages_to_watermark: List of page indices (0-based) to watermark. If None, watermark all pages.
    :raises FileNotFoundError: If the input file or image does not exist.
    """
    validate_file_path(input_path)
    validate_file_path(image_path)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Create a watermark PDF
    watermark_pdf = BytesIO()
    c = canvas.Canvas(watermark_pdf, pagesize=letter)
    c.drawImage(image_path, 100, 100, width=200, height=100, mask="auto")  # Position and size the watermark
    c.save()

    # Apply the watermark to the specified pages
    watermark_reader = PdfReader(watermark_pdf)
    watermark_page = watermark_reader.pages[0]

    for i in range(len(reader.pages)):
        page = reader.pages[i]
        if pages_to_watermark is None or i in pages_to_watermark:
            page.merge_page(watermark_page)
        writer.add_page(page)

    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)

def remove_watermark(input_path, output_path, pages_to_clean=None):
    """
    Remove watermarks from all or specific pages of a PDF.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the cleaned PDF.
    :param pages_to_clean: List of page indices (0-based) to clean. If None, clean all pages.
    :raises FileNotFoundError: If the input file does not exist.
    """
    validate_file_path(input_path)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for i in range(len(reader.pages)):
        page = reader.pages[i]
        if pages_to_clean is None or i in pages_to_clean:
            # Create a new page without the watermark
            new_page = PdfWriter()
            new_page.add_page(page)
            with BytesIO() as temp_pdf:
                new_page.write(temp_pdf)
                temp_pdf.seek(0)
                new_reader = PdfReader(temp_pdf)
                writer.add_page(new_reader.pages[0])
        else:
            writer.add_page(page)

    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)