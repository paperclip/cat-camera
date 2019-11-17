#!/bin/env python

import csv
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

def getSize(f):
    statbuf = os.stat(f)
    return statbuf.st_size

def main(argv):
    os.chdir(r"C:\Users\windo\Documents\camera")

    catDir = os.path.join("images","cat")

    cats = list(os.listdir(catDir))
    cats.sort(reverse=True)
    notcats = list(os.listdir(os.path.join("images","not_cat")))
    notcats.sort(reverse=True)

    ## Run predict on all

    c = label_image.ImageClassify()

    def generateImages(limit=10):
        l = limit
        for imagename in cats:
            yield True, os.path.join(catDir,imagename)
            l -= 1
            if l % 100 == 0:
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

    resultsCsvFile = open("accuracy.csv","w",newline='')
    resultsCsv = csv.writer(resultsCsvFile)
    resultsCsv.writerow(("IsCat","PredictedCat","Size","Basename"))

    for (actuallyCat, src) in generateImages(10000):
        try:
            best_label, cat_result, resultMap = c.predict_image(src)
            if actuallyCat:
                actuallyCatResults.append(cat_result)
            else:
                actuallyNotCatResults.append(cat_result)
            resultsCsv.writerow((str(actuallyCat),cat_result,getSize(src),os.path.basename(src)))
        except Exception as e:
            print("Failed to process %s"%src)
            print(e)

    resultsCsvFile.close()

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
