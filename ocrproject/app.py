from flask import Flask, request, jsonify
from main import run_ocr
from pdf2image import convert_from_path
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/ocr', methods=['POST'])
def ocr_endpoint():
    try:
        file = request.files['image']
        print("Received file:", file.filename)

        filename = file.filename
        ext = filename.lower().split('.')[-1]
        print("File extension:", ext)

        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        results = []

        if ext == 'pdf':
            images = convert_from_path(path)
            for img in images:
                ocr_result = run_ocr(img)
                print("OCR result for page:", ocr_result)
                results.extend(ocr_result if isinstance(ocr_result, list) else [ocr_result])
        else:
            # ✅ Always open image with PIL before passing to run_ocr
            with Image.open(path) as img:
                ocr_result = run_ocr(img)
                print("OCR result:", ocr_result)
                results.extend(ocr_result if isinstance(ocr_result, list) else [ocr_result])

        os.remove(path)
        return jsonify({'text': results})

    except Exception as e:
        print("Error in OCR route:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(port=5000, debug=True)