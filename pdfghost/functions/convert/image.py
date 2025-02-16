# pdfghost/functions/convert/image.py


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


def images_to_pdf(output_path, *image_paths):
    """
    Convert multiple image files into a single PDF using Pillow.

    :param output_path: Path to save the output PDF.
    :param image_paths: Paths of the image files to convert.
    :raises FileNotFoundError: If any input image file does not exist.
    """
