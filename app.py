import os
from flask import Flask, redirect, render_template, request, send_from_directory, url_for
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image 
from tensorflow.keras.models import load_model
import numpy as np
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the trained model
model = keras.models.load_model('./model_baru.keras')

# Define the image size
img_height = 224
img_width = 224

# Define the list of possible predictions
possible_predictions = [
 'Kawung',
 'Parang',
 'Sidoluhur',
 'Truntum',
 'Tumpal']

# Define the home page route
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return render_template('index.html', prediction="No image uploaded")

    # Get the uploaded image
    image_file = request.files['image']
    
    if image_file.filename == '':
        return render_template('index.html', prediction="No selected file")

    # Save the image to the uploads folder
    filename = secure_filename(image_file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_file.save(image_path)

    try:
        # Load the image and preprocess it
        img = image.load_img(image_path, target_size=(img_height, img_width))
        img_array = image.img_to_array(img) / 255.0

        # Make the prediction
        prediction = model.predict(np.expand_dims(img_array, axis=0))[0]
        
        # Convert prediction to percentages
        prediction_percentages = {possible_predictions[i]: float(prediction[i] * 100) for i in range(len(possible_predictions))}
        
        # Get the predicted class index and name
        predicted_class_index = np.argmax(prediction)
        predicted_class_name = possible_predictions[predicted_class_index]
        
        # Set a threshold for valid prediction
        threshold = 90.0  # Example threshold percentage
        if prediction_percentages[predicted_class_name] < threshold:
            predicted_class_name = "prediksi tidak ada dimodel"

    except Exception as e:
        predicted_class_name = f"Error: {str(e)}"
        prediction_percentages = {}

    # Return the prediction and the image URL
    return render_template('index.html', prediction=predicted_class_name, image_url=url_for('static', filename='uploads/' + filename), prediction_percentages=prediction_percentages)

@app.route('/static/uploads', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file', filename=filename))

# # Function to serve the uploaded file
# @app.route('/static/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
