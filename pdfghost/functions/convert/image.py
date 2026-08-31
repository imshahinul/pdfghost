# pdfghost/functions/convert/image.py
import os
import tempfile
import pymupdf
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
    pdf_document = pymupdf.open(input_path)

    # Convert each page to an image
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        mat = pymupdf.Matrix(zoom, zoom)  # Zoom factor for higher resolution
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
    if not image_paths:
        raise ValueError("At least one image path is required.")

    for path in image_paths:
        validate_file_path(path)

    images = []
    temporary_path = None
    try:
        for path in image_paths:
            with Image.open(path) as image:
                image.load()
                images.append(image.convert("RGB"))

        output_directory = os.path.dirname(os.fspath(output_path)) or "."
        with tempfile.NamedTemporaryFile(
            dir=output_directory, suffix=".pdf", delete=False
        ) as temporary_file:
            temporary_path = temporary_file.name
        images[0].save(
            temporary_path,
            save_all=True,
            append_images=images[1:],
            format="PDF",
            resolution=72.0,
        )
        os.replace(temporary_path, output_path)
        temporary_path = None
    finally:
        for image in images:
            image.close()
        if temporary_path is not None and os.path.exists(temporary_path):
            os.remove(temporary_path)
