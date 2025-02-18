# pdfghost/functions/pdf_signature.py
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject
from PyPDF2.generic import create_string_object
from ..utils.path_validator import validate_file_path

def sign_pdf(input_path: str, output_path: str, certificate_path: str, password: str = None):
    """
    Add a digital signature to a PDF using a cryptographic certificate.

    :param input_path: Path to the input PDF file.
    :param output_path: Path to save the signed PDF file.
    :param certificate_path: Path to the cryptographic certificate file.
    :param password: Password for the certificate (if required).
    :raises FileNotFoundError: If the input file or certificate does not exist.
    :raises ValueError: If the certificate is invalid or the signing process fails.
    """
    validate_file_path(input_path)
    validate_file_path(certificate_path)

    # Read the input PDF
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Add the digital signature
    with open(certificate_path, "rb") as cert_file:
        certificate = cert_file.read()

    # Add the signature annotation
    writer.add_annotation(
        page_number=0,
        annotation={
            "/Type": NameObject("/Annot"),
            "/Subtype": NameObject("/Widget"),
            "/FT": NameObject("/Sig"),
            "/Rect": [0, 0, 0, 0],  # Invisible signature
            "/V": create_string_object(certificate),
            "/T": create_string_object("Signature1"),
            "/F": 4,
            "/P": writer.get_page(0).indirect_reference,
        },
    )

    # Save the signed PDF
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)