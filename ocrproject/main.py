import pytesseract

def run_ocr(file_path):
    """
    Simple OCR function using pytesseract on a file path.
    Works for images and PDFs (one page at a time).
    """
    text = pytesseract.image_to_string(file_path)
    return text.strip()


if __name__ == "__main__":
    path = input("Enter path to image or PDF page image: ").strip()
    print("OCR output:\n")
    print(run_ocr(path))
