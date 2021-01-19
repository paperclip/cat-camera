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
import time

import tensorflow1.camera_dir
tensorflow1.camera_dir.cd_camera_dir()
import tensorflow1.utils
safemkdir = tensorflow1.utils.safemkdir

import database.db

## Reclassify images into the new_cat directory

import label_image as classifier
c = classifier.ImageClassify()
model_version = "classify1_%d" % int(c.m_model_version)

def newCat():
    for base in range(100,-1,-1):
        directory = os.path.join("new_cat","%02d"%base)
        if not os.path.isdir(directory):
            continue
        pics = os.listdir(directory)
        for p in pics:
            yield os.path.join(directory,p)


def inner_main(db, argv):
    pending = list(newCat())
    remaining = len(pending)
    print("Total=", remaining)
    start = time.time()
    last_commit = time.time()
    todo = remaining
    if len(argv) > 1:
        todo = int(argv[1])
    for src in pending:
        n = os.path.basename(src)
        try:
            _, catPercentage, resultMap = c.predict_image(src)
            dest = os.path.join("new_cat", "%02d" % (int(catPercentage*100)))
            db.addValue(n, model_version, float(catPercentage * 100))
            safemkdir(dest)
            dest = os.path.join(dest, n)
            if src != dest:
                print("%s\t%s\t%s\t%d" %
                      (src, str(resultMap), dest, remaining))
                os.rename(src, dest)
            remaining -= 1
            duration = time.time() - last_commit
            if duration > 60:
                print("db commit:", duration)
                db.commit()
                last_commit = time.time()
            todo -= 1
            if todo <= 0:
                break
        except EnvironmentError as e:
            print("Failed to process %s" % src)
            print(e)
        except Exception as e:
            print("Failed to process %s" % src)
            print(e)
            raise

    end = time.time()
    duration = end - start
    print("Duration:", duration)


def main(argv):
    with database.db.Database() as db:
        inner_main(db, argv)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
