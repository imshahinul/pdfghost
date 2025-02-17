# pdfghost/functions/encryption.py
from PyPDF2 import PdfReader, PdfWriter
from ..utils.path_validator import validate_file_path


def encrypt_pdf(input_path, output_path, password):
    """
    Encrypt a PDF with a password.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the encrypted PDF.
    :param password: Password to encrypt the PDF.
    :raises FileNotFoundError: If the input file does not exist.
    """
    validate_file_path(input_path)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Encrypt the PDF
    writer.encrypt(password)

    # Save the encrypted PDF
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)


def decrypt_pdf(input_path, output_path, password):
    """
    Decrypt a PDF with a password.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the decrypted PDF.
    :param password: Password to decrypt the PDF.
    :raises FileNotFoundError: If the input file does not exist.
    :raises ValueError: If the password is incorrect.
    """
    validate_file_path(input_path)

    reader = PdfReader(input_path)

    # Check if the PDF is encrypted
    if not reader.is_encrypted:
        raise ValueError("The PDF is not encrypted.")

    # Try to decrypt the PDF
    if not reader.decrypt(password):
        raise ValueError("Incorrect password.")

    writer = PdfWriter()

    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Save the decrypted PDF
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)
