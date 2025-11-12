# utils/ocr_utils.py

from PIL import Image
import pytesseract

def ocr_image(file_path):
    """
    Perform OCR on an image and return extracted text.
    """
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text
