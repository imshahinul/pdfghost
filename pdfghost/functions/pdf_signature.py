# pdfghost/functions/pdf_signature.py

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