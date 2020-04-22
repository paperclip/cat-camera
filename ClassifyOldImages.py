#!/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow
import shutil
import subprocess
import sys
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tensorflow.get_logger().setLevel('ERROR')

import database.db
db = database.db.Database()

catDir = os.path.join("images","cat")
cats = os.listdir(catDir)
cats.sort(reverse=True)


notcatsDir = os.path.join("images","not_cat")
notcats = os.listdir(notcatsDir)
notcats.sort(reverse=True)

assert len(cats) > 0
assert len(notcats) > 0

print("Cat images %d"%len(cats))
print("Not cat images %d"%len(notcats))

import label_image as classifier
c = classifier.ImageClassify()
model_version = "classify1_%d" % int(c.m_model_version)

truePositive = 0
trueNegative = 0
falsePostive = 0
falseNegative = 0

remaining = len(cats) + len(notcats)

if len(sys.argv) > 1:
    count = int(sys.argv[1])
else:
    count = 100

try:
    for i in cats[:count]:
        before = time.time()
        src = os.path.join(catDir, i)
        record = db.getRecord(i, 'cat', 1)
        if record.get(model_version, None) is None:
            newPredict = "NEW"
            topLabel, catPercentage, resultMap = c.predict_image(src)
            catPercentage = catPercentage * 100
            record[model_version] = float(catPercentage)
            db.updateRecord(record)
        else:
            newPredict = ""
            catPercentage = record[model_version]
        duration = time.time() - before
        if catPercentage >= 50:
            truePositive += 1
            print("%3f" % duration, i, newPredict, "TruePositive", remaining, catPercentage)
        else:
            falseNegative += 1
            print("%3f" % duration, i, newPredict, "FalseNegative", remaining,
                  catPercentage)
        remaining -= 1

    for i in notcats[:count]:
        before = time.time()
        src = os.path.join(notcatsDir, i)
        record = db.getRecord(i, 'cat', 0)
        if record.get(model_version, None) is None:
            newPredict = "NEW"
            topLabel, catPercentage, resultMap = c.predict_image(src)
            catPercentage = catPercentage * 100
            record[model_version] = float(catPercentage)
            db.updateRecord(record)
        else:
            newPredict = ""
            catPercentage = record[model_version]
        duration = time.time() - before

        if catPercentage < 50:
            trueNegative +=1
            print("%3f" % duration, i, newPredict, "TrueNegative", remaining,
                 catPercentage)
        else:
            falsePostive += 1
            print("%3f" % duration, i, newPredict, "FalsePositive", remaining,
                  catPercentage)
        remaining -= 1
except KeyboardInterrupt as e:
    pass
finally:
    db.close()

    print("True Positive  = %d"%truePositive)
    print("True Negative  = %d"%trueNegative)
    print("False Positive = %d"%falsePostive)
    print("False Negative = %d"%falseNegative)
    print()

    if truePositive + falseNegative > 0:
        print("Recall = %f"% (1.0*truePositive / (truePositive + falseNegative)))
    if truePositive + falsePostive > 0:
        print("Precision = %f"%(1.0*truePositive / (truePositive + falsePostive)))
