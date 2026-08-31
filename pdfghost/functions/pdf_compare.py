# pdfghost/functions/pdf_compare.py
from itertools import zip_longest

from pypdf import PdfReader
from termcolor import colored
from ..utils.path_validator import validate_file_path


def compare_pdfs(file1: str, file2: str, output_type: str = "summary"):
    """
    Compare two PDF files and identify differences.

    :param file1: Path to the first PDF file.
    :param file2: Path to the second PDF file.
    :param output_type: Type of comparison output ("summary", "side_by_side", "highlight_differences", "version_control", "annotations").
    :raises FileNotFoundError: If either input file does not exist.
    :return: A string containing the comparison result.
    """
    valid_output_types = {
        "summary",
        "side_by_side",
        "highlight_differences",
        "version_control",
        "annotations",
    }
    if not isinstance(output_type, str):
        raise TypeError("output_type must be a string")
    output_type = output_type.lower()
    if output_type not in valid_output_types:
        raise ValueError(f"output_type must be one of {sorted(valid_output_types)}")

    validate_file_path(file1)
    validate_file_path(file2)

    def read_pdf(file):
        """Extract text from a PDF file."""
        reader = PdfReader(file)
        return "".join((page.extract_text() or "") + "\n" for page in reader.pages)

    def compared_lines(text1, text2):
        return enumerate(
            zip_longest(text1.splitlines(), text2.splitlines(), fillvalue=""),
            1,
        )

    def side_by_side_comparison(text1, text2):
        """Generate a side-by-side comparison of two texts."""
        output = ""
        for _, (line1, line2) in compared_lines(text1, text2):
            output += f"{line1:<60} | {line2:<60}\n"
        return output

    def highlight_differences(text1, text2):
        """Highlight differences between two texts."""
        output = ""
        for _, (line1, line2) in compared_lines(text1, text2):
            if line1 != line2:
                output += f"{colored(line1, 'red')} | {colored(line2, 'green')}\n"
            else:
                output += f"{line1:<60} | {line2:<60}\n"
        return output

    def summary_section(text1, text2):
        """Generate a summary of differences between two texts."""
        summary = "Summary of Differences:\n"
        for line_number, (line1, line2) in compared_lines(text1, text2):
            if line1 != line2:
                summary += f"- Line {line_number}: File 1: {line1}, File 2: {line2}\n"
        return summary

    def version_control(text1, text2):
        """Generate a version control-style comparison of two texts."""
        changes = "Changes:\n"
        for line_number, (line1, line2) in compared_lines(text1, text2):
            if line1 != line2:
                changes += f"  - Line {line_number}: {line1}\n"
                changes += f"  + Line {line_number}: {line2}\n"
        return changes

    def annotations(text1, text2):
        """Generate annotations for differences between two texts."""
        annotations = "Annotations:\n"
        for line_number, (line1, line2) in compared_lines(text1, text2):
            if line1 != line2:
                annotations += f"  * Note: Line {line_number} differs\n"
        return annotations

    # Extract text from both PDFs
    text1 = read_pdf(file1)
    text2 = read_pdf(file2)

    # Generate the comparison result based on the output type
    if output_type == "side_by_side":
        result = side_by_side_comparison(text1, text2)
    elif output_type == "highlight_differences":
        result = highlight_differences(text1, text2)
    elif output_type == "summary":
        result = summary_section(text1, text2)
    elif output_type == "version_control":
        result = version_control(text1, text2)
    elif output_type == "annotations":
        result = annotations(text1, text2)

    return result
