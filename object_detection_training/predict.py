#!/bin/env python3

import pandas as pd

import numpy as np
import tensorflow as tf
from tensorflow import keras
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# from matplotlib import rc
# from pandas.plotting import register_matplotlib_converters
# from sklearn.model_selection import train_test_split
import urllib
import os
import csv
# import cv2
import time
# from PIL import Image

# CLASSES_FILE = 'annotations/'
# labels_to_names = pd.read_csv(
#   CLASSES_FILE,
#   header=None
# ).T.loc[0].to_dict()

model = keras.models.load_model(r"trained-inference-graphs\output_inference_graph_v1.pb\saved_model")
# print(model.summary())

IMG_WIDTH = 299
IMG_HEIGHT = 299

def decode_img(img):
  # convert the compressed string to a 3D uint8 tensor
  img = tf.image.decode_jpeg(img, channels=3)
  # Use `convert_image_dtype` to convert to floats in the [0,1] range.
  img = tf.image.convert_image_dtype(img, tf.float32)
  # resize the image to the desired size.
  return tf.image.resize(img, [IMG_WIDTH, IMG_HEIGHT])

def process_path(file_path):
  # load the raw data from the file as a string
  img = tf.io.read_file(file_path)
  img = decode_img(img)
  return img

def predict(image):
  image = process_path(image)

  boxes, scores, labels = model.predict_on_batch(
    np.expand_dims(image, axis=0)
  )

  scale = 1.0
  boxes /= scale

  return boxes, scores, labels

import sys
print(predict(sys.argv[1]))
