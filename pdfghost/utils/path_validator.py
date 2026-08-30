# pdfghost/utils/path_validator.py
import os


def validate_file_path(path):
    """
    Validate that a path exists and refers to a regular file.

    :param path: Path to the file.
    :raises FileNotFoundError: If the path does not exist.
    :raises IsADirectoryError: If the path refers to a directory.
    :raises ValueError: If the path exists but is not a regular file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist.")

    if os.path.isdir(path):
        raise IsADirectoryError(f"The path {path} is a directory, not a file.")

    if not os.path.isfile(path):
        raise ValueError(f"The path {path} is not a regular file.")


def validate_directory_path(path):
    """
    Ensure that a path refers to an output directory.

    Missing directories are created recursively.

    :param path: Path to the directory.
    :raises NotADirectoryError: If an existing path is not a directory.
    """
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise NotADirectoryError(f"The path {path} is not a directory.")
        return

    os.makedirs(path)


def validate_existing_directory_path(path):
    """
    Validate that a required input directory already exists.

    :param path: Path to the existing directory.
    :raises FileNotFoundError: If the directory does not exist.
    :raises NotADirectoryError: If the path exists but is not a directory.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory {path} does not exist.")

    if not os.path.isdir(path):
        raise NotADirectoryError(f"The path {path} is not a directory.")
