# pdfghost/functions/pdf_compare.py


def compare_pdfs(file1: str, file2: str, output_type: str = "summary"):
    """
    Compare two PDF files and identify differences.

    :param file1: Path to the first PDF file.
    :param file2: Path to the second PDF file.
    :param output_type: Type of comparison output ("summary", "side_by_side", "highlight_differences", "version_control", "annotations").
    :raises FileNotFoundError: If either input file does not exist.
    :return: A string containing the comparison result.
    """
