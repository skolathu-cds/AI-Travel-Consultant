import os
from PyPDF2 import PdfReader
from docx import Document

def read_travel_policy(file_path):
    """
    Reads the travel policy document from the given file path.
    Supports both PDF and Word formats.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.endswith(".pdf"):
        return read_pdf(file_path)
    elif file_path.endswith(".docx"):
        return read_word(file_path)
    else:
        raise ValueError("Unsupported file format. Please use a .pdf or .docx file.")

def read_pdf(file_path):
    """
    Reads text from a PDF file.
    """
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_word(file_path):
    """
    Reads text from a Word document.
    """
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text