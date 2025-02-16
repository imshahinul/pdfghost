# pdfghost/functions/convert/image.py
import os
import fitz  # PyMuPDF
from PIL import Image
from ...utils.path_validator import validate_file_path, validate_directory_path


def pdf_to_images(input_path, output_folder, format="png", zoom=2):
    """
    Convert each page of a PDF into an image (PNG/JPG/JPEG) using PyMuPDF.

    :param input_path: Path to the input PDF.
    :param output_folder: Folder to save the output images.
    :param format: Output image format ("png", "jpg", or "jpeg").
    :param zoom: Zoom factor for higher resolution images.
    :raises FileNotFoundError: If the input file does not exist.
    :raises ValueError: If the output format is invalid.
    """
    validate_file_path(input_path)
    validate_directory_path(output_folder)

    if format.lower() not in ["png", "jpg", "jpeg"]:
        raise ValueError("Output format must be 'png', 'jpg', or 'jpeg'.")

    # Open the PDF file
    pdf_document = fitz.open(input_path)

    # Convert each page to an image
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        mat = fitz.Matrix(zoom, zoom)  # Zoom factor for higher resolution
        pix = page.get_pixmap(matrix=mat)
        image_path = os.path.join(output_folder, f"page_{page_number + 1}.{format}")
        pix.save(image_path)


def images_to_pdf(output_path, *image_paths):
    """
    Convert multiple image files into a single PDF using Pillow.

    :param output_path: Path to save the output PDF.
    :param image_paths: Paths of the image files to convert.
    :raises FileNotFoundError: If any input image file does not exist.
    """
    images = []
    for path in image_paths:
        validate_file_path(path)
        images.append(Image.open(path))

    # Save images as a single PDF
    images[0].save(output_path, save_all=True, append_images=images[1:], format="PDF")
