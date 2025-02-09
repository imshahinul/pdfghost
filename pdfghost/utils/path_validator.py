# pdfghost/utils/path_validator.py
import os

def validate_file_path(path):
    """
    Validate if the file path exists.

    :param path: Path to the file.
    :raises FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist.")

def validate_directory_path(path):
    """
    Validate if the directory path exists. If not, create it.

    :param path: Path to the directory.
    """
    if not os.path.exists(path):
        os.makedirs(path)