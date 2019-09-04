#!/usr/bin/env python


from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import sys
import random
import os

HEIGHT = 300
WIDTH = 300
# dimensions of our images
img_width, img_height = WIDTH, HEIGHT

def loadModel(model_name):
    model_file_name = "keras2/cat_model_{}.h5".format(model_name)
    # load the model we saved
    model = load_model(model_file_name)
    # model.compile(loss='binary_crossentropy',
    #               optimizer='rmsprop',
    #               metrics=['accuracy'])

    # predicting images
    return model

batch_size = 10

TOTAL = 0
CAT_TOTAL = 0.0
NOT_CAT_TOTAL = 0.0
MODEL = None

def predict_images(imagenames):
    global TOTAL
    global CAT_TOTAL
    global NOT_CAT_TOTAL
    images = []
    for i in imagenames:
        img = image.load_img(i, target_size=(img_width, img_height))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        # x /= 255.
        images.append(x)

    images = np.vstack(images)
    classes = MODEL.predict(images, batch_size=batch_size)

    for i in range(len(classes)):
        print(imagenames[i],classes[i])
        TOTAL += 1
        CAT_TOTAL += classes[i][0]
        NOT_CAT_TOTAL += classes[i][1]

def run(argv):
    # predict_images(sys.argv[1:])
    if len(argv) > 2:
        model_name = argv[2]
    else:
        model_name = "ResNet50"

    global MODEL
    MODEL = loadModel(model_name)

    testdir = argv[1]
    contents = os.listdir(testdir)
    random.shuffle(contents)

    i = 0
    while i < len(contents):
        predict_images([ os.path.join(testdir, f) for f in contents[i:i+batch_size]])
        i += batch_size


try:
    run(sys.argv)
finally:
    print("TOTAL:",TOTAL)
    print("    Cat average:", (CAT_TOTAL / TOTAL))
    print("Not Cat average:", (NOT_CAT_TOTAL / TOTAL))

#
# # predicting multiple images at once
# img = image.load_img('test2.jpg', target_size=(img_width, img_height))
# y = image.img_to_array(img)
# y = np.expand_dims(y, axis=0)
#
# # pass the list of multiple images np.vstack()
# images = np.vstack([x, y])
# classes = model.predict_classes(images, batch_size=10)
#
# # print the classes, the images belong to
# print classes
# print classes[0]
# print classes[0][0]
