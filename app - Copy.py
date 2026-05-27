import os
from flask import Flask, render_template, request, jsonify
from google.cloud import vision
from werkzeug.utils import secure_filename

# 🔑 Set path to your downloaded key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\mrudu\Documents\Marathi_text\key\marathi-ocr-468003-b3206f46593d.json"

# 🎯 Initialize Flask and Google Vision client
app = Flask(__name__)
vision_client = vision.ImageAnnotatorClient()

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    image_bytes = file.read()

    # 📷 Vision OCR request
    image = vision.Image(content=image_bytes)
    response = vision_client.text_detection(image=image)

    texts = response.text_annotations
    if not texts:
        return jsonify({'marathi_text': ''})

    marathi_text = texts[0].description.strip()

    return jsonify({'marathi_text': marathi_text})

if __name__ == '__main__':
    app.run(debug=True)