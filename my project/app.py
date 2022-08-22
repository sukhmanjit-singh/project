from flask import Flask, flash, request, redirect, url_for, render_template,make_response
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2 as cv
import base64
import numpy as np
import urllib

app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def make_grayscale(in_stream):
    arr = np.fromstring(in_stream, dtype='uint8')

    img = cv.imdecode(arr, cv.IMREAD_UNCHANGED)

    # Make grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    _, out_stream = cv.imencode('.jpg', gray)

    return out_stream
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_data = make_grayscale(file.read())
        flash('Image successfully uploaded and displayed below')
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename),'wb') as f:
            f.write(file_data)

        return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')
    # else:
    #     flash('Allowed image types are - png, jpg, jpeg, gif')
    #     return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
if __name__ == "__main__":
    app.run()
