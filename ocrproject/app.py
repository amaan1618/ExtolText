from flask import Flask, request, jsonify
from ocr_utils import run_ocr, run_ocr_pdf
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/ocr', methods=['POST'])
def ocr_endpoint():
    try:
        file = request.files['image']
        filename = file.filename
        ext = filename.lower().split('.')[-1]

        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        if ext == 'pdf':
            with open(path, 'rb') as f:
                pdf_bytes = f.read()
            text = run_ocr_pdf(pdf_bytes)
        else:
            img = Image.open(path)
            text = run_ocr(img)

        os.remove(path)
        return jsonify({'text': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(port=5000, debug=True)
