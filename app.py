from flask import Flask, render_template, request, jsonify
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import tensorflow as tf
import cv2
import numpy as np
from medicines import MedicineFilter
app = Flask(__name__)
# Load trained model
model = tf.keras.models.load_model('chest_xray_2.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/about-us')
def aboutus():
    return render_template('aboutus.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if request contains file
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        # Read and preprocess the image
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        resized_img = cv2.resize(img, (224, 224))
        img_array = image.img_to_array(resized_img)
        expanded_img_array = np.expand_dims(img_array, axis=0)
        preprocessed_img = preprocess_input(expanded_img_array)

        # Perform prediction using the model
        classes = model.predict(preprocessed_img)

        # Assuming binary classification, determine the class based on the probability
        prediction = "Pneumonia Detected Please seek Medical Advice" if classes[0][0] > 0.5 else "No Pneumonia detected"

    

        # Return result and filtered medicines as JSON-serializable data
        return jsonify({'result': prediction})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/medications')
def get_medications():
    med_filter = MedicineFilter('medicines.csv')
    medications = med_filter.filter_medicines()
    return jsonify({'medications': medications})

if __name__ == '__main__':
    app.run(debug=True)
