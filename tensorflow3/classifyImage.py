

import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    from . import mobilenet_v2
except ImportError:
    import mobilenet_v2

import tensorflow as tf

IMG_WIDTH = 224
IMG_HEIGHT = 224

model = mobilenet_v2.MobileNetV2Base(include_top=True)

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

for arg in sys.argv[1:]:
    logger.info("Predicting on %s",arg)
    img = process_path(arg)
    prediction = model.predict(img)
    logger.info("Result for %s = %s",arg, prediction)
