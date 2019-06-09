#!/bin/env python

import os
import shutil
import subprocess
import sys

## rsync -va douglas@pi:webdata/camera/ camera

RSYNC=r"F:\cygwin64\bin\rsync"

os.chdir(r"C:\Users\windo\Documents\camera")

# subprocess.call([RSYNC,"-va","douglas@pi:webdata/camera/","camera"])

catDir = os.path.join("images","cat")

cats = set(os.listdir(catDir))
notcats = set(os.listdir(os.path.join("images","not_cat")))


assert len(cats) > 0
assert len(notcats) > 0

print("Cat images %d"%len(cats))
print("Not cat images %d"%len(notcats))

def safemkdir(d):
    try:
        os.makedirs(d)
    except EnvironmentError:
        pass

import label_image as classifier
c = classifier.ImageClassify()

truePositive = 0
truePositiveTotal = 0.0
trueNegative = 0
trueNegativeTotal = 0.0
falsePositive = 0
falsePositiveTotal = 0.0
falseNegative = 0
falseNegativeTotal = 0.0

limit = 10000

for imagename in cats:
    src = os.path.join(catDir,imagename)
    try:
        results = c.predict_image(src)
        print(src,results,limit)
        if results[0] == "cat":
            truePositive += 1
            truePositiveTotal += results[1][0]
        else:
            falseNegative += 1
            falseNegativeTotal += results[1][0]
        limit -= 1
        if limit == 0:
            break
    except Exception as e:
        print("Failed to process %s"%src)
        print(e)

limit = 10000

for imagename in notcats:
    src = os.path.join("images","not_cat",imagename)
    try:
        results = c.predict_image(src)
        print(src,results,limit)
        if results[0] == "cat":
            falsePositive += 1
            falsePositiveTotal += results[1][0]
        else:
            trueNegative += 1
            trueNegativeTotal += results[1][0]
        limit -= 1
        if limit == 0:
            break
    except Exception as e:
        print("Failed to process %s"%src)
        print(e)

print("True Positive  = %d"%truePositive)
print("True Negative  = %d"%trueNegative)
print("False Positive = %d"%falsePositive)
print("False Negative = %d"%falseNegative)
print("True Positive Average  = %f"%(truePositiveTotal / truePositive))
print("True Negative Average  = %f"%(trueNegativeTotal / trueNegative))
print("False Positive Average = %f"%(falsePositiveTotal / falsePositive))
print("False Negative Average = %f"%(falseNegativeTotal / falseNegative))
print("Cat Average     = %f"%((truePositiveTotal + falseNegativeTotal)/(truePositive+falseNegative)))
print("Not Cat Average = %f"%((trueNegativeTotal + falsePositiveTotal)/(trueNegative+falsePositive)))
print()
if truePositive + falseNegative > 0:
    print("Recall = %f"% (1.0*truePositive / (truePositive + falseNegative)))
if truePositive + falsePositive > 0:
    print("Precision = %f"%(1.0*truePositive / (truePositive + falsePositive)))
