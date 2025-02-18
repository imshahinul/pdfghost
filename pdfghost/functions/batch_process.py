# pdfghost/functions/batch_process.py
from typing import Callable


def batch_process(input_folder: str, output_folder: str, operation: Callable, **kwargs):
    """
    Apply a specified operation to all PDFs in a folder.

    :param input_folder: Path to the folder containing input PDFs.
    :param output_folder: Path to the folder to save processed PDFs.
    :param operation: Function to apply to each PDF (e.g., merge, split, rotate).
    :param kwargs: Additional arguments to pass to the operation function.
    :raises FileNotFoundError: If the input folder does not exist.
    """
