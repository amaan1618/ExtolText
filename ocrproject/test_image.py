from PIL import Image

image_path = r"C:\Users\neett\Desktop\test.jpg"

try:
    img = Image.open(image_path)
    img.show()
    print("✅ Image opened successfully with PIL.")
except Exception as e:
    print("❌ PIL failed to open the image:", e)