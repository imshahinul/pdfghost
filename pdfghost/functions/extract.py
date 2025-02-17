# pdfghost/functions/extract.py
import os
import csv
from PyPDF2 import PdfReader
from ..utils.path_validator import validate_file_path, validate_directory_path


def extract_text(input_path, output_path, format="txt"):
    """
    Extract text from a PDF file and save it as a .txt or .csv file.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the extracted text.
    :param format: Output format ("txt" or "csv").
    :raises FileNotFoundError: If the input file does not exist.
    :raises ValueError: If the output format is invalid.
    """
    validate_file_path(input_path)

    if format.lower() not in ["txt", "csv"]:
        raise ValueError("Output format must be 'txt' or 'csv'.")

    reader = PdfReader(input_path)
    text = ""

    # Extract text from all pages
    for page in reader.pages:
        text += page.extract_text()

    # Save the extracted text
    if format.lower() == "txt":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
    elif format.lower() == "csv":
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Text"])
            for line in text.splitlines():
                writer.writerow([line])


def extract_images(input_path, output_folder):
    """
    Extract all images from a PDF and save them as separate image files.

    :param input_path: Path to the input PDF.
    :param output_folder: Folder to save the extracted images.
    :raises FileNotFoundError: If the input file does not exist.
    """
    validate_file_path(input_path)
    validate_directory_path(output_folder)

    reader = PdfReader(input_path)

    # Extract images from all pages
    for page_number, page in enumerate(reader.pages):
        for image_number, image in enumerate(page.images):
            image_path = os.path.join(output_folder,
                                      f"page_{page_number + 1}_image_{image_number + 1}.{image.name.split('.')[-1]}")
            with open(image_path, "wb") as f:
                f.write(image.data)
