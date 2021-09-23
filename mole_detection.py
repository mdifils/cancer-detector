# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 01:41:59 2021

@author: michel
"""

import os
import numpy as np
import streamlit as st
from PIL import Image
# from mole_preprocessing import image_preparation
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# creating two containers
header = st.container()
main = st.container()

# grabbing the current directory
cwd = os.getcwd()

def load_image(image_file):
    img = Image.open(image_file)
    return img

def image_preparation(img_path: str, img_size: tuple) -> np.ndarray:
    
    # Load your image
    img = image.load_img(img_path, target_size=img_size)
    
    # Convert your image pixels to a numpy array of values. 
    img = image.img_to_array(img)
    
    # reshape your image dimensions.
    img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])
    # img = np.expand_dims(img, axis=0)
    
    # preprocess your image with preprocess_input
    prepared_img = preprocess_input(img)
    return prepared_img

def delete_images():
    for file in os.listdir(cwd):
        if file.endswith('.jpg'):
            os.remove(file)
        elif file.endswith('.png'):
            os.remove(file)

model = load_model('Mobilenet_model', compile=False)

with header:
    st.title("Melona Detection")
    # grab the uploaded image
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])

if image_file:
    # delete all previous images stored in the current directory
    delete_images()
    # store the uploaded image in the current directory
    with open(image_file.name, "wb") as f:
        f.write(image_file.getbuffer())
    # prepare the uploaded image for the prediction
    sample = image_preparation(image_file.name, (224,224))
    # predict
    prediction = model.predict(sample.reshape(1,224,224,3))
    result = np.argmax(prediction, axis=-1)[0]
    # conclusion
    if result == 1:
        label = "Bad news, this is a cancerous skin lesion."
    else:
        label = "Good news, this lesion is benign."
    
    with main:
        st.header("Result")
        # create two columns
        col1, col2 = st.columns(2)

        col1.success("Image")
        # display the uploaded image
        col1.image(load_image(image_file))

        col2.success("Prediction")
        # write the conclusion about the prediction
        col2.text(label)