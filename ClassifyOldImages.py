#!/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import subprocess
import time
import tinydb

catDir = os.path.join("images","cat")
cats = os.listdir(catDir)


notcatsDir = os.path.join("images","not_cat")
notcats = os.listdir(notcatsDir)

assert len(cats) > 0
assert len(notcats) > 0

print("Cat images %d"%len(cats))
print("Not cat images %d"%len(notcats))

import label_image as classifier
c = classifier.ImageClassify()

truePositive = 0
trueNegative = 0
falsePostive = 0
falseNegative = 0

remaining = len(cats) + len(notcats)

try:
    for i in cats:
        src = os.path.join(catDir,i)
        before = time.time()
        results = c.predict_image(src)
        duration = time.time() - before
        if results[0] == "cat":
            truePositive += 1
            print(duration,i,"TruePositive",remaining,results)
        else:
            falseNegative += 1
            print(duration,i,"FalseNegative",remaining,results)
        remaining -= 1

    for i in notcats:
        src = os.path.join(notcatsDir,i)
        before = time.time()
        results = c.predict_image(src)
        duration = time.time() - before
        if results[0] == "not cat":
            trueNegative +=1
            print(duration,i,"TrueNegative",remaining,results)
        else:
            falsePostive += 1
            print(duration,i,"FalsePositive",remaining,results)
        remaining -= 1
except KeyboardInterrupt as e:
    pass
finally:
    print("True Positive  = %d"%truePositive)
    print("True Negative  = %d"%trueNegative)
    print("False Positive = %d"%falsePostive)
    print("False Negative = %d"%falseNegative)
    print()

    if truePositive + falseNegative > 0:
        print("Recall = %f"% (1.0*truePositive / (truePositive + falseNegative)))
    if truePositive + falsePostive > 0:
        print("Precision = %f"%(1.0*truePositive / (truePositive + falsePostive)))
