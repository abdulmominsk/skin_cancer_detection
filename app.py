from __future__ import division, print_function

import os
import numpy as np

# Keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'Skin_Cancer_Model.h5'

# Load your trained model
model = load_model(MODEL_PATH)

lesion_classes_dict = {
    0 : 'Melanocytic nevi',
    1 : 'Melanoma',
    2 : 'Benign keratosis-like lesions ',
    3 : 'Basal cell carcinoma',
    4 : 'Actinic keratoses',
    5 : 'Vascular lesions',
    6 : 'Dermatofibroma'
}



def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(64, 64))

    # Preprocessing the image
    
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        # Process your result for human
        pred_class = preds.argmax(axis=-1)
        pr = lesion_classes_dict[pred_class]
        result =str(pr) 
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)
