# pdfghost/functions/pdf_compare.py
from PyPDF2 import PdfReader
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
    validate_file_path(file1)
    validate_file_path(file2)

    def read_pdf(file):
        """Extract text from a PDF file."""
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def side_by_side_comparison(text1, text2):
        """Generate a side-by-side comparison of two texts."""
        text1_lines = text1.splitlines()
        text2_lines = text2.splitlines()
        max_lines = max(len(text1_lines), len(text2_lines))
        output = ""
        for i in range(max_lines):
            line1 = text1_lines[i] if i < len(text1_lines) else ""
            line2 = text2_lines[i] if i < len(text2_lines) else ""
            output += f"{line1:<60} | {line2:<60}\n"
        return output

    def highlight_differences(text1, text2):
        """Highlight differences between two texts."""
        text1_lines = text1.splitlines()
        text2_lines = text2.splitlines()
        max_lines = max(len(text1_lines), len(text2_lines))
        output = ""
        for i in range(max_lines):
            line1 = text1_lines[i] if i < len(text1_lines) else ""
            line2 = text2_lines[i] if i < len(text2_lines) else ""
            if line1 != line2:
                output += f"{colored(line1, 'red')} | {colored(line2, 'green')}\n"
            else:
                output += f"{line1:<60} | {line2:<60}\n"
        return output

    def summary_section(text1, text2):
        """Generate a summary of differences between two texts."""
        summary = "Summary of Differences:\n"
        text1_lines = text1.splitlines()
        text2_lines = text2.splitlines()
        for i in range(min(len(text1_lines), len(text2_lines))):
            if text1_lines[i] != text2_lines[i]:
                summary += f"- Line {i + 1}: File 1: {text1_lines[i]}, File 2: {text2_lines[i]}\n"
        return summary

    def version_control(text1, text2):
        """Generate a version control-style comparison of two texts."""
        changes = "Changes:\n"
        text1_lines = text1.splitlines()
        text2_lines = text2.splitlines()
        for i in range(min(len(text1_lines), len(text2_lines))):
            if text1_lines[i] != text2_lines[i]:
                changes += f"  - Line {i + 1}: {text1_lines[i]} -> {text2_lines[i]}\n"
        return changes

    def annotations(text1, text2):
        """Generate annotations for differences between two texts."""
        annotations = "Annotations:\n"
        text1_lines = text1.splitlines()
        text2_lines = text2.splitlines()
        for i in range(min(len(text1_lines), len(text2_lines))):
            if text1_lines[i] != text2_lines[i]:
                annotations += f"  * Note: Line {i + 1} differs\n"
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
    else:
        result = summary_section(text1, text2)

    return result
