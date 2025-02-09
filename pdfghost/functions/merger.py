# pdfghost/functions/merger.py


def merge_pdfs(output_path, *input_paths):
    """
    Merge multiple PDFs into a single PDF.

    :param output_path: Path to save the merged PDF.
    :param input_paths: Paths of the PDFs to merge.
    :raises FileNotFoundError: If any input file does not exist.
    """
    # Validate input file paths