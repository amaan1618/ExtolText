import cv2
import numpy as np
import pytesseract
import json
from PIL import Image
from ocr_utils import deskew, preprocess, detect_text_regions

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\neett\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def run_ocr(image_input):
    # Load image using PIL and convert to OpenCV format
    if isinstance(image_input, str):
        print("🔍 Trying to load image from:", image_input)
        try:
            pil_img = Image.open(image_input)
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            print("✅ Image loaded successfully via PIL.")
        except Exception as e:
            raise ValueError(f"❌ PIL failed to load image: {e}")
    else:
        img = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)

    img = deskew(img)
    binary = preprocess(img)
    boxes = detect_text_regions(binary)

    results = []
    for (x, y, w, h) in boxes:
        roi = binary[y:y+h, x:x+w]
        raw_text = pytesseract.image_to_string(roi, config='--oem 1 --psm 6').strip()
        corrected = raw_text
        data = {
            'raw': raw_text,
            'corrected': corrected,
            'box': [x, y, w, h]
        }
        results.append(data)

    return results

if __name__ == '__main__':
    print("ocr running")
    image_path = r"C:\Users\neett\Desktop\Frontend For Project\ocrproject\test.jpg"
    output = run_ocr(image_path)
    print(json.dumps(output, indent=2))