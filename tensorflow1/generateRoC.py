#!/bin/env python

import json
import os
import sys
import numpy as np
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

try:
    import label_image
    import findIndex
except ImportError:
    from . import label_image
    from . import findIndex

def main(argv):
    os.chdir(r"C:\Users\windo\Documents\camera")

    catDir = os.path.join("images","cat")

    cats = set(os.listdir(catDir))
    notcats = set(os.listdir(os.path.join("images","not_cat")))

    ## Run predict on all

    c = label_image.ImageClassify()

    def generateImages(limit=10):
        l = limit
        for imagename in cats:
            yield True, os.path.join(catDir,imagename)
            l -= 1
            if l %100 == 0:
                print("Done %d cat"%(limit -l))
            if l == 0:
                break

        l = limit
        for imagename in notcats:
            yield False, os.path.join("images","not_cat",imagename)
            l -= 1
            if l %100 == 0:
                print("Done %d not cat"%(limit -l))
            if l == 0:
                break

    actuallyCatResults = []
    actuallyNotCatResults = []

    for (actuallyCat, src) in generateImages(3000):
        try:
            best_label, cat_result, resultMap = c.predict_image(src)
            if actuallyCat:
                actuallyCatResults.append(cat_result)
            else:
                actuallyNotCatResults.append(cat_result)
        except Exception as e:
            print("Failed to process %s"%src)
            print(e)

    actuallyCatResults.sort()
    actuallyNotCatResults.sort()
    print(actuallyCatResults, actuallyNotCatResults)

    results = []

    actualCatsDivisor = 0
    notCatsDivisor = 0

    for n in range(1,99):
        actualCatsDivisor = findIndex.findIndex(actuallyCatResults, n / 100, actualCatsDivisor)
        falseNegative = actualCatsDivisor / len(actuallyCatResults)
        truePositive = 1 - falseNegative
        print("+", n, actualCatsDivisor, falseNegative, truePositive)

        notCatsDivisor = findIndex.findIndex(actuallyNotCatResults, n / 100, notCatsDivisor)
        trueNegative = notCatsDivisor / len(actuallyNotCatResults)
        falsePositive = 1 - trueNegative
        print("-", n, notCatsDivisor, trueNegative, falsePositive)

        results.append((falsePositive, truePositive))

    open("roc.json","w").write(json.dumps(results))
    print(results)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
