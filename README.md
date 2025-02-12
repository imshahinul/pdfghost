# PDF Ghost

`PDF Ghost` is a Python library designed for performing a wide range of operations on PDF files, including merging,
splitting, rotating, compressing, watermarking, converting, encrypting/decrypting, extracting text/images, adding page
numbers, batch processing, and comparing PDFs. It also supports generating PDFs from Markdown or LaTeX files.

## Features

- **Merge PDFs**: Combine multiple PDFs into a single file.
- **Split PDFs**: Split a PDF into smaller files based on page ranges.
- **Remove Pages**: Remove specific pages with page index, remove page from start and end.
- **Rotate Pages**: Rotate all or specific pages in a PDF.
- **Insert Pages**: Insert pages or specific pages in a PDF.
- **Rearrange Pages**: Rearrange pages of a pdf file or merge pdf files and then rearrange all the pages.
- **Compress PDFs**: Reduce the file size of a PDF by optimizing images and removing unnecessary metadata.

## Installation

### Python Requirements

- Python 3.7+

### Install via pip

```bash
pip install pdfghost
```

## Usage

### Merge PDFs

```python
from pdfghost import merge_pdfs

merge_pdfs("output.pdf", "file1.pdf", "file2.pdf")
```

### Split PDF

```python
from pdfghost import split_pdf

split_pdf("input.pdf", "output_folder", split_range=(0, 2))
```

### Remove Specific Pages

```python
from pdfghost import remove_pages

# Remove pages with indices 0, 2, and 4 (0-based)
remove_pages("input.pdf", "output.pdf", pages_to_remove=[0, 2, 4])
```

### Remove Pages from Start

```python
from pdfghost import remove_pages_from_start

# Remove the first 3 pages
remove_pages_from_start("input.pdf", "output.pdf", num_pages=3)
```

### Remove Pages from End

```python
from pdfghost import remove_pages_from_end

# Remove the last 2 pages
remove_pages_from_end("input.pdf", "output.pdf", num_pages=2)
```

### Rotate Pages

```python
from pdfghost import rotate_pdf

# Rotate all pages by 90 degrees
rotate_pdf("input.pdf", "output.pdf", rotation=90)

# Rotate specific pages by 180 degrees
rotate_pdf("input.pdf", "output.pdf", rotation=180, pages_to_rotate=[0, 2])
```

### Insert Pages

```python
from pdfghost import insert_pages

# Insert pages at specific positions
insertions = [
    (1, "insert1.pdf"),  # Insert pages from insert1.pdf at position 1
    (4, "insert2.pdf"),  # Insert pages from insert2.pdf at position 4
]
insert_pages("input.pdf", "output.pdf", insertions)
```

### Rearrange Pages

```python
from pdfghost import rearrange_pdf

# Rearrange pages in a PDF
page_order = [2, 0, 1]  # New order: Page 3, Page 1, Page 2
rearrange_pdf("input.pdf", "output.pdf", page_order)
```

### Merge and Rearrange Pages

```python
from pdfghost import merge_and_rearrange

# Merge multiple PDFs and rearrange their pages
page_order = [
    (0, 0),  # Page 1 from file1.pdf
    (1, 0),  # Page 1 from file2.pdf
    (0, 1),  # Page 2 from file1.pdf
]
merge_and_rearrange("output.pdf", page_order, "file1.pdf", "file2.pdf")
```

### Compress PDF

```python
from pdfghost import compress_pdf

# Compress a PDF with medium compression
compress_pdf("input.pdf", "output.pdf", power=3)

# Compress a PDF with maximum compression
compress_pdf("input.pdf", "output.pdf", power=5)
```

## Testing

To run unit tests, first install the development dependencies, and then use:

```bash
python -m unittest discover tests/
```

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.