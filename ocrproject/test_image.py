import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\Users\amaan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

img = cv2.imread("hq720.jpg")

text = pytesseract.image_to_string(img)

print(text)
