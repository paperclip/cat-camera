
import matplotlib.pylab as plt

import tensorflow as tf
import tensorflow_hub as hub

from tensorflow.keras import optimizers
from tensorflow.keras import layers
import tensorflow.keras.backend as K
import numpy as np
import PIL.Image as Image

import os
import sys
import time

import tensorflow.keras

try:
    import model_constants
except ImportError:
    from . import model_constants

model_name = model_constants.model_name
feature_extractor_url = model_constants.feature_extractor_url

model = tensorflow.keras.models.load_model(model_constants.saved_model_name)
print(model)

image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

BASE = u"C:/Users/windo/Documents/camera"

IMAGE_SIZE = hub.get_expected_image_size(hub.Module(feature_extractor_url))

data_root = u"{}/images".format(BASE)
cat_dir = os.path.join(data_root, "cat")
#
# image_data = image_generator.flow_from_directory(str(data_root), target_size=IMAGE_SIZE)
#
# for image_batch,label_batch in image_data:
#     print("Image batch shape: ", image_batch.shape)
#     print("Labe batch shape: ", label_batch.shape)
#     break
#
# label_names = sorted(image_data.class_indices.items(), key=lambda pair:pair[1])
# label_names = np.array([key.title() for key, value in label_names])
# print(label_names)
#
#
# result_batch = model.predict(image_batch)
# print(result_batch)
# labels_batch = label_names[np.argmax(result_batch, axis=-1)]
# print(labels_batch)

cats = os.listdir(cat_dir)
cats.sort()
COUNT=500
totals = [0,0]
for c in cats[-COUNT:]:
    p = os.path.join(cat_dir, c)
    image = tf.keras.preprocessing.image.load_img(p, target_size=IMAGE_SIZE)
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

    pred = model.predict(image)
    print("cat",c,pred)
    totals[0] += pred[0][0]

not_cat_dir = os.path.join(data_root, "not_cat")
images = os.listdir(not_cat_dir)
images.sort()
for c in images[-COUNT:]:
    p = os.path.join(not_cat_dir, c)
    image = tf.keras.preprocessing.image.load_img(p, target_size=IMAGE_SIZE)
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

    pred = model.predict(image)
    print("not cat",c,pred)
    totals[1] += pred[0][0]

print(totals)
