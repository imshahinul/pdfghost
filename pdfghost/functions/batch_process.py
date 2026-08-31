# pdfghost/functions/batch_process.py
import os
from typing import Callable
from ..utils.path_validator import (
    validate_directory_path,
    validate_existing_directory_path,
)


def batch_process(input_folder: str, output_folder: str, operation: Callable, **kwargs):
    """
    Apply a specified operation to all PDFs in a folder.

    :param input_folder: Path to the folder containing input PDFs.
    :param output_folder: Path to the folder to save processed PDFs.
    :param operation: Function to apply to each PDF (e.g., merge, split, rotate).
    :param kwargs: Additional arguments to pass to the operation function.
    :raises FileNotFoundError: If the input folder does not exist.
    """
    if not callable(operation):
        raise TypeError("operation must be callable")

    validate_existing_directory_path(input_folder)
    if os.path.realpath(input_folder) == os.path.realpath(output_folder):
        raise ValueError("input_folder and output_folder must be different")

    pdf_files = sorted(
        (
            file_name
            for file_name in os.listdir(input_folder)
            if file_name.lower().endswith(".pdf")
            and os.path.isfile(os.path.join(input_folder, file_name))
        ),
        key=lambda file_name: (file_name.casefold(), file_name),
    )

    if not pdf_files:
        raise FileNotFoundError("No PDF files found in the input folder.")

    validate_directory_path(output_folder)

    # Apply the operation to each PDF
    for pdf_file in pdf_files:
        input_path = os.path.join(input_folder, pdf_file)
        output_path = os.path.join(output_folder, pdf_file)

        # Call the operation function
        operation(input_path, output_path, **kwargs)
