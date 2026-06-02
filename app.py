import os
from flask import Flask, request, render_template
from google.cloud import vision
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Cloud credentials are now loaded from the GOOGLE_APPLICATION_CREDENTIALS
# environment variable defined in your .env file. Do NOT hardcode the path here.

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Run OCR via Google Cloud Vision
    client = vision.ImageAnnotatorClient()
    with open(filepath, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    extracted_text = texts[0].description if texts else 'No text found.'

    image_url = f'/static/uploads/{filename}'
    return render_template('result.html', image_url=image_url, translated_text=extracted_text)

if __name__ == '__main__':
    app.run(debug=True)