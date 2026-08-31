# pdfghost/functions/watermark.py
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO
import warnings
from ..utils.path_validator import validate_file_path


_PAGE_SELECTION_TYPES = (list, tuple, set, frozenset)


def _validate_pages_to_watermark(pages_to_watermark, page_count):
    if pages_to_watermark is None:
        return None
    if not isinstance(pages_to_watermark, _PAGE_SELECTION_TYPES):
        raise TypeError(
            "pages_to_watermark must be None or a list, tuple, set, or frozenset"
        )

    pages = set()
    for page_index in pages_to_watermark:
        if isinstance(page_index, bool) or not isinstance(page_index, int):
            raise TypeError("page indices must be integers excluding bool")
        if page_index < 0 or page_index >= page_count:
            raise ValueError("page index out of range")
        pages.add(page_index)
    return pages


def _text_watermark_page(width, height, text):
    packet = BytesIO()
    watermark = canvas.Canvas(packet, pagesize=(width, height))
    watermark.setFont("Helvetica", 60)
    watermark.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.5)
    watermark.drawCentredString(width / 2, height / 2, text)
    watermark.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]


def _image_watermark_page(width, height, image_path):
    packet = BytesIO()
    watermark = canvas.Canvas(packet, pagesize=(width, height))
    watermark.drawImage(
        image_path,
        (width - 200) / 2,
        (height - 100) / 2,
        width=200,
        height=100,
        mask="auto",
    )
    watermark.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

def add_text_watermark(input_path, output_path, text, pages_to_watermark=None):
    """
    Add a text watermark to all or specific pages of a PDF.

    :param input_path: Path to the input PDF.
    :param output_path: Path to save the watermarked PDF.
    :param text: Text to use as the watermark.
    :param pages_to_watermark: List of page indices (0-based) to watermark. If None, watermark all pages.
    :raises FileNotFoundError: If the input file does not exist.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    validate_file_path(input_path)

    reader = PdfReader(input_path)
    selected_pages = _validate_pages_to_watermark(
        pages_to_watermark, len(reader.pages)
    )
    writer = PdfWriter(clone_from=reader)

    for index, page in enumerate(writer.pages):
        if selected_pages is None or index in selected_pages:
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            page.merge_page(_text_watermark_page(width, height, text))

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
    validate_file_path(image_path)
    validate_file_path(input_path)

    reader = PdfReader(input_path)
    selected_pages = _validate_pages_to_watermark(
        pages_to_watermark, len(reader.pages)
    )
    writer = PdfWriter(clone_from=reader)

    for index, page in enumerate(writer.pages):
        if selected_pages is None or index in selected_pages:
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            page.merge_page(_image_watermark_page(width, height, image_path))

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
    if pages_to_clean is not None:
        if not isinstance(pages_to_clean, _PAGE_SELECTION_TYPES):
            raise TypeError(
                "pages_to_clean must be None or a list, tuple, set, or frozenset"
            )
        for page_index in pages_to_clean:
            if isinstance(page_index, bool) or not isinstance(page_index, int):
                raise TypeError("page indices must be integers excluding bool")

    warnings.warn(
        "remove_watermark is deprecated because reliable removal of arbitrary "
        "or merged watermark content is unavailable.",
        DeprecationWarning,
        stacklevel=2,
    )
    raise NotImplementedError(
        "reliable removal of arbitrary or merged watermark content is unavailable; "
        "no output was created."
    )
