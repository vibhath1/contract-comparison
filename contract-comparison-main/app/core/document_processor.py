import os
import mimetypes
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from docx import Document
import pdfplumber

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_image(file_path):
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)

def extract_text_from_scanned_pdf(file_path):
    text = ""
    pages = convert_from_path(file_path)
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".pdf":
        try:
            # Try native text extraction
            text = extract_text_from_pdf(file_path)
            if not text.strip():
                raise ValueError("Empty text, try OCR.")
            return text
        except:
            # Fallback to OCR
            return extract_text_from_scanned_pdf(file_path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
