from __future__ import absolute_import, division, print_function

import matplotlib.pylab as plt

import tensorflow as tf
import tensorflow_hub as hub

import tensorflow.keras
from tensorflow.keras import optimizers
from tensorflow.keras import layers
import tensorflow.keras.backend as K
import numpy as np
import PIL.Image as Image

import os
import sys
import time

try:
    import model_constants
except ImportError:
    from . import model_constants

BASE = u"C:/Users/windo/Documents/camera"

data_root = u"{}/images".format(BASE)

image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
# image_data = image_generator.flow_from_directory(str(data_root))
#
# for image_batch,label_batch in image_data:
#   print("Image batch shape: ", image_batch.shape)
#   print("Labe batch shape: ", label_batch.shape)
#   break

model_name = model_constants.model_name
feature_extractor_url = model_constants.feature_extractor_url

def feature_extractor(x):
  feature_extractor_module = hub.Module(feature_extractor_url)
  return feature_extractor_module(x)

IMAGE_SIZE = hub.get_expected_image_size(hub.Module(feature_extractor_url))
image_data = image_generator.flow_from_directory(str(data_root), target_size=IMAGE_SIZE)
for image_batch,label_batch in image_data:
    print("Image batch shape: ", image_batch.shape)
    print("Labe batch shape: ", label_batch.shape)
    break

features_extractor_layer = layers.Lambda(feature_extractor, input_shape=IMAGE_SIZE+[3])
features_extractor_layer.trainable = False

model = tf.keras.Sequential([
  features_extractor_layer,
  layers.Dense(image_data.num_classes, activation='softmax')
])
print(model.summary())

sess = K.get_session()
init = tf.global_variables_initializer()
sess.run(init)

optimizer = optimizers.Adam()
model.compile(
  optimizer=optimizer,
  loss='categorical_crossentropy',
  metrics=['accuracy'])

class CollectBatchStats(tf.keras.callbacks.Callback):
  def __init__(self):
    self.batch_losses = []
    self.batch_acc = []

  def on_batch_end(self, batch, logs=None):
    self.batch_losses.append(logs['loss'])
    self.batch_acc.append(logs['acc'])

EPOCHS = 2
steps_per_epoch = image_data.samples//image_data.batch_size
batch_stats = CollectBatchStats()
history = model.fit_generator(image_data, epochs=EPOCHS,
                    steps_per_epoch=steps_per_epoch,
                    callbacks = [batch_stats])

print(history)

model.save("cat_model_{}.h5".format(model_name))

plt.figure()
plt.ylabel("Loss")
plt.xlabel("Training Steps")
plt.ylim([0,2])
plt.plot(batch_stats.batch_losses)

plt.figure()
plt.ylabel("Accuracy")
plt.xlabel("Training Steps")
plt.ylim([0,1])
plt.plot(batch_stats.batch_acc)

plt.show()
