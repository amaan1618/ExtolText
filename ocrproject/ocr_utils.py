import cv2
import numpy as np
import pytesseract
from PIL import Image

def load_image(path_or_pil):
    """
    Load image from path (str) or PIL.Image.Image object.
    Returns OpenCV BGR image.
    """
    if isinstance(path_or_pil, str):
        img = cv2.imread(path_or_pil)
        if img is None:
            raise ValueError(f"Cannot load image from path: {path_or_pil}")
        return img
    elif isinstance(path_or_pil, Image.Image):
        return cv2.cvtColor(np.array(path_or_pil), cv2.COLOR_RGB2BGR)
    else:
        raise TypeError("Input must be file path or PIL.Image.Image")

def deskew(img):
    """
    Deskew the image using its grayscale moments.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = np.column_stack(np.where(gray < 255))
    if coords.size == 0:
        return img  # empty image, return as-is
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle += 90
    (h, w) = img.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

def preprocess(img):
    """
    Convert image to grayscale, blur, threshold, and clean using morphology.
    Ensures black text on white background.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    # Invert if background is dark
    if np.mean(thresh) < 127:
        thresh = cv2.bitwise_not(thresh)

    # Morphological open to remove small noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    return cleaned

def detect_text_regions(binary_img):
    """
    Detect text regions using contour detection.
    Returns a sorted list of bounding boxes (x, y, w, h).
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(binary_img, kernel, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 30 and h > 15:  # filter tiny boxes
            boxes.append((x, y, w, h))
    return sorted(boxes, key=lambda b: b[1])  # sort top to bottom

def extract_text_from_regions(img, boxes):
    """
    Run Tesseract OCR on each detected text region.
    Returns combined text.
    """
    texts = []
    for (x, y, w, h) in boxes:
        roi = img[y:y+h, x:x+w]
        text = pytesseract.image_to_string(
            roi,
            config='--oem 3 --psm 6'
        )
        if text.strip():
            texts.append(text.strip())
    return "\n".join(texts)

def run_full_ocr(path_or_pil):
    """
    Main OCR function compatible with your Django/Flask app.
    Accepts file path (str) or PIL.Image.
    Returns extracted text string.
    """
    img = load_image(path_or_pil)
    img = deskew(img)
    binary = preprocess(img)
    boxes = detect_text_regions(binary)
    text = extract_text_from_regions(img, boxes)
    return text.strip()
