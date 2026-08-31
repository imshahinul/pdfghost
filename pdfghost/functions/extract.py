# pdfghost/functions/extract.py
import os
import csv
import tempfile
from pypdf import PdfReader
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
    if not isinstance(format, str):
        raise TypeError("format must be a string")
    normalized_format = format.lower()
    if normalized_format not in ["txt", "csv"]:
        raise ValueError("Output format must be 'txt' or 'csv'.")

    validate_file_path(input_path)
    reader = PdfReader(input_path)
    text = "".join(page.extract_text() or "" for page in reader.pages)

    output_directory = os.path.dirname(os.fspath(output_path)) or "."
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=output_directory,
            encoding="utf-8",
            newline="",
            delete=False,
        ) as output_file:
            temporary_path = output_file.name
            if normalized_format == "txt":
                output_file.write(text)
            else:
                writer = csv.writer(output_file)
                writer.writerow(["Text"])
                for line in text.splitlines():
                    writer.writerow([line])
        os.replace(temporary_path, output_path)
        temporary_path = None
    finally:
        if temporary_path is not None and os.path.exists(temporary_path):
            os.remove(temporary_path)


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
