import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes

# Make sure pytesseract points to your tesseract exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\neett\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def run_ocr(img):
    """
    img: PIL.Image.Image
    Returns extracted text as a string
    """
    text = pytesseract.image_to_string(img)
    return text.strip()

def run_ocr_pdf(pdf_bytes):
    """
    pdf_bytes: bytes object from uploaded PDF
    Returns combined text from all pages
    """
    images = convert_from_bytes(pdf_bytes)
    all_text = ""
    for img in images:
        all_text += run_ocr(img) + "\n\n"
    return all_text.strip()
