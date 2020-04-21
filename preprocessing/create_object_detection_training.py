#!/bin/env python3

# import tensorflow1.camera_dir
# tensorflow1.camera_dir.cd_camera_dir()

import os
import shutil
import sys

srcdir = "images/cat"
src_files = os.listdir(srcdir)

dest = "object_detection_2"
images = os.path.join(dest,"images")
training_images = os.path.join(images, "train")
test_images = os.path.join(images, "test")

def safe_mkdir(p):
    try:
        os.makedirs(p)
    except EnvironmentError:
        pass

safe_mkdir(training_images)
safe_mkdir(test_images)

TRAINING_COUNT = 0
TEST_COUNT = 0

def isTraining():
    global TRAINING_COUNT
    global TEST_COUNT
    if TRAINING_COUNT * 20 > TEST_COUNT * 80:
        TEST_COUNT += 1
        return False
    TRAINING_COUNT += 1
    return True

# annotations_src = "annotations"
# existing_annotations = os.listdir(annotations_src)
# assert len(existing_annotations) > 0
#
# for annotation in existing_annotations:
#     print(annotation)
#     image = annotation.replace(".xml", ".jpeg")
#     assert image in src_files
#     d = training_images if isTraining() else test_images
#     shutil.copy(os.path.join(annotations_src, annotation), os.path.join(d, annotation))

if len(sys.argv) > 1:
    count = int(sys.argv[1])
else:
    count = 100

src_files.sort(reverse=True)
for f in src_files:
    if os.path.isfile(os.path.join(training_images, f)):
        continue
    if os.path.isfile(os.path.join(test_images, f)):
        continue
    d = training_images if isTraining() else test_images
    print(f, d, TRAINING_COUNT, TEST_COUNT)
    shutil.copy(os.path.join(srcdir, f), os.path.join(d, f))
    count -= 1
    if count == 0:
        break
