# modules/text_extraction.py

import pdfplumber
import docx
from PIL import Image
import pytesseract
from pathlib import Path

def extract_text_from_pdf(file_path):
    text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
    return "\n".join(text)

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_image(file_path):
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text

def extract_text(file_path):
    """Detect file type and extract text"""
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        return extract_text_from_docx(file_path)
    elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        return extract_text_from_image(file_path)
    else:
        # fallback: treat as plain text
        return Path(file_path).read_text(encoding="utf-8", errors="ignore")
