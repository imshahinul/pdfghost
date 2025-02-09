# pdfghost/functions/merger.py
from PyPDF2 import PdfMerger
from ..utils.path_validator import validate_file_path


def merge_pdfs(output_path, *input_paths):
    """
    Merge multiple PDFs into a single PDF.

    :param output_path: Path to save the merged PDF.
    :param input_paths: Paths of the PDFs to merge.
    :raises FileNotFoundError: If any input file does not exist.
    """
    # Validate input file paths
    for path in input_paths:
        validate_file_path(path)

    merger = PdfMerger()

    for path in input_paths:
        merger.append(path)

    merger.write(output_path)
    merger.close()
