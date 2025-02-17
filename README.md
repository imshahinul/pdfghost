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
- **Watermarking**: Add or remove text or image watermarks to PDFs.
- **Image to PDF**: Covert Images to PDF file.
- **PDF to Image**: Convert pages of a PDF file to images.
- **Encrypt/Decrypt PDFs**: Add password protection to PDFs and decrypt them with the correct password.
- **Extract Text/Images**: Extract text or images from a PDF.
- **Add Page Numbers**: Insert page numbers at the bottom or top of each page.
- **Convert PDFs to HTML**: Convert PDFs into structured HTML files.

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

### Add Text Watermark

```python
from pdfghost import add_text_watermark

# Add a text watermark to all pages
add_text_watermark("input.pdf", "output.pdf", text="Confidential")

# Add a text watermark to specific pages
add_text_watermark("input.pdf", "output.pdf", text="Confidential", pages_to_watermark=[0, 2])
```

### Add Image Watermark

```python
from pdfghost import add_image_watermark

# Add an image watermark to all pages
add_image_watermark("input.pdf", "output.pdf", image_path="watermark.png")

# Add an image watermark to specific pages
add_image_watermark("input.pdf", "output.pdf", image_path="watermark.png", pages_to_watermark=[1])
```

### Remove Watermark

```python
from pdfghost import remove_watermark

# Remove watermarks from all pages
remove_watermark("input.pdf", "output.pdf")

# Remove watermarks from specific pages
remove_watermark("input.pdf", "output.pdf", pages_to_clean=[0, 2])
```

### Convert PDF to Images

```python
from pdfghost import pdf_to_images

# Convert each page of a PDF into PNG images
pdf_to_images("input.pdf", "output_folder", format="png")

# Convert each page of a PDF into JPG images
pdf_to_images("input.pdf", "output_folder", format="jpg")
```

### Convert Images to PDF

```python
from pdfghost import images_to_pdf

# Convert multiple image files into a single PDF
images_to_pdf("output.pdf", "image1.png", "image2.jpg")
```

### Encrypt PDF

```python
from pdfghost import encrypt_pdf

# Encrypt a PDF with a password
encrypt_pdf("input.pdf", "output.pdf", password="mypassword")
```

### Decrypt PDF

```python
from pdfghost import decrypt_pdf

# Decrypt a PDF with a password
decrypt_pdf("input.pdf", "output.pdf", password="mypassword")
```

### Extract Text

```python
from pdfghost import extract_text

# Extract text from a PDF and save it as a .txt file
extract_text("input.pdf", "output.txt", format="txt")

# Extract text from a PDF and save it as a .csv file
extract_text("input.pdf", "output.csv", format="csv")
```

### Extract Images

```python
from pdfghost import extract_images

# Extract all images from a PDF and save them as separate image files
extract_images("input.pdf", "output_folder")
```

### Add Page Numbers
```python
from pdfghost import add_page_numbers

# Add page numbers at the bottom of each page
add_page_numbers("input.pdf", "output.pdf", position="bottom")

# Add page numbers at the top of each page
add_page_numbers("input.pdf", "output.pdf", position="top")
```

### Convert PDF to HTML
```python
from pdfghost import pdf_to_html

# Convert a PDF into a structured HTML file
pdf_to_html("input.pdf", "output.html")
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