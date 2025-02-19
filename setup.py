from setuptools import setup, find_packages

setup(
    name="pdf-ghost",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "cffi==1.17.1",
        "chardet==5.2.0",
        "charset-normalizer==3.4.1",
        "cryptography==44.0.1",
        "pdfminer.six==20231228",
        "pdfplumber==0.11.5",
        "pillow==11.1.0",
        "pycparser==2.22",
        "PyMuPDF==1.25.3",
        "PyPDF2==3.0.1",
        "pypdfium2==4.30.1",
        "reportlab==4.3.0",
        "termcolor==2.5.0",
    ],
    author="S M Shahinul Islam",
    author_email="s.m.shahinul.islam@gmail.com@gmail.com",
    description="for performing a wide range of operations on PDF files, including merging, splitting, rotating, compressing, watermarking, converting, encrypting/decrypting, extracting text/images, adding page numbers, batch processing, and comparing PDFs. It also supports generating PDFs from Markdown or LaTeX files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/imshahinul/pdfghost",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
