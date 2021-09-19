import numpy as np
import cv2
import os
import pandas as pd
from pathlib import Path
from PIL import ImageEnhance, Image
from skimage import feature
import pickle



# Load pickle file
with open("pickle_model_asl.pkl", 'rb') as file:
    pickle_model = pickle.load(file)

#loaded_scaler
with open("pickle_scaler_asl.pkl", 'rb') as file:
    pickle_scaler = pickle.load(file)

#loaded_label
with open("pickle_label_asl.pkl", 'rb') as file:
    pickle_le = pickle.load(file)



 # this function to extract features from image
def quantify_image(image):
  frame = cv2.resize(image, (400,400))
  height, width, channels = frame.shape
  upper_left = (width // 4, height // 4)
  bottom_right = (width * 3 // 4, height * 3 // 4)
  rect_img = frame[upper_left[1]: bottom_right[1] + 1, upper_left[0]: bottom_right[0] + 1]
  # show the skin in the image along with the mask
  edges = cv2.Canny(rect_img,100,200)
  features = feature.hog(image, orientations=9,pixels_per_cell=(10, 10), 
                         cells_per_block=(2, 2),transform_sqrt=True, block_norm="L1")
  # return the feature vector
  return features


#predict Asl
#load image using opencv (donot forget to change this path and add your image path)
# check if image read
# convert image color to RGB
#resize image
#generate features using quntify function
#scale features using pickle_scaler object
# predict label using pickle_model object
#get class name from pickle_le objecy
def ai_cap():
    image = cv2.imread("ai.png")
    if image is not None:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (400, 400))
        fet = quantify_image(image)
        fet_sca = pickle_scaler.transform([fet])
        pred = pickle_model.predict(fet_sca)
        label = pickle_le.classes_[pred[0]]
        print(label)
        return label