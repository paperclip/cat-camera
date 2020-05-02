#!/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow
tensorflow.get_logger().setLevel('ERROR')

import sys
import re
import tensorflow1.camera_dir
tensorflow1.camera_dir.cd_camera_dir()
import tensorflow1.utils
safemkdir = tensorflow1.utils.safemkdir

import database.db

## Reclassify images into the new_cat directory

import label_image as classifier
c = classifier.ImageClassify()
model_version = "classify1_%d" % int(c.m_model_version)

db = database.db.Database()

def newCat():
    for base in range(100,-1,-1):
        directory = os.path.join("new_cat","%02d"%base)
        if not os.path.isdir(directory):
            continue
        pics = os.listdir(directory)
        for p in pics:
            yield os.path.join(directory,p)


def inner_main():
    pending = list(newCat())
    remaining = len(pending)
    print("Total=", remaining)
    for src in pending:
        n = os.path.basename(src)
        try:
            _, catPercentage, resultMap = c.predict_image(src)
            dest = os.path.join("new_cat", "%02d" % (int(catPercentage*100)))
            db.addValue(n, model_version, float(catPercentage * 100))
            safemkdir(dest)
            dest = os.path.join(dest, os.path.basename(src))
            if src != dest:
                print("%s\t%s\t%s\t%d" %
                      (src, str(resultMap), dest, remaining))
                os.rename(src, dest)
            remaining -= 1
        except EnvironmentError as e:
            print("Failed to process %s" % src)
            print(e)
        except Exception as e:
            print("Failed to process %s" % src)
            print(e)
            raise

def main(argv):
    try:
        inner_main()
    finally:
        db.close()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
