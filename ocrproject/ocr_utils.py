# ocr_utils.py
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes

# If on Windows, ensure this path points to your tesseract.exe
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def run_ocr(img):
    """
    Runs pytesseract on a PIL.Image image.
    Returns text as a string.
    """
    return pytesseract.image_to_string(img, lang='eng').strip()

def run_ocr_pdf(pdf_bytes):
    """
    Accepts PDF as bytes, converts each page to an image, runs OCR.
    Returns combined text.
    """
    pages = convert_from_bytes(pdf_bytes)
    text = ""
    for page in pages:
        text += run_ocr(page) + "\n\n"
    return text.strip()
