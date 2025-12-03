import cv2
import numpy as np
import pytesseract
from PIL import Image

def load_image(path_or_pil):
    """Load image from path or PIL image."""
    if isinstance(path_or_pil, Image.Image):
        return cv2.cvtColor(np.array(path_or_pil), cv2.COLOR_RGB2BGR)
    else:
        img = cv2.imread(path_or_pil)
        if img is None:
            raise ValueError(f"Cannot load image from path: {path_or_pil}")
        return img

def deskew(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = np.column_stack(np.where(gray < 255))
    if coords.size == 0:
        return img  # nothing to deskew
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle += 90
    (h, w) = img.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC)

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    return cleaned

def detect_text_regions(binary_img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(binary_img, kernel, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 30 and h > 15:
            boxes.append((x, y, w, h))
    return sorted(boxes, key=lambda b: b[1])

def extract_text_from_regions(img, boxes):
    texts = []
    for (x, y, w, h) in boxes:
        roi = img[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, config='--psm 6').strip()
        if text:
            texts.append(text)
    return "\n".join(texts)

# This is the function your views expect
def run_full_ocr(path_or_pil):
    img = load_image(path_or_pil)
    img = deskew(img)
    binary = preprocess(img)
    boxes = detect_text_regions(binary)
    return extract_text_from_regions(img, boxes)
