#!/bin/env python

import csv
import json
import os
import sys
import numpy as np
import tensorflow as tf
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

try:
    import label_image
    import findIndex
    import generate_roc_data
    import camera_dir
except ImportError:
    from . import label_image
    from . import findIndex
    from . import generate_roc_data
    from . import camera_dir

def getSize(f):
    statbuf = os.stat(f)
    return statbuf.st_size

def call_generate_roc_data(actuallyCatResults, actuallyNotCatResults):
    results = generate_roc_data.generate_roc_data(actuallyCatResults, actuallyNotCatResults)
    open("roc.json","w").write(json.dumps(results))
    print(results)

    return 0

def main(argv):
    camera_dir.cd_camera_dir()

    catDir = os.path.join("images","cat")

    cats = list(os.listdir(catDir))
    cats.sort(reverse=True)
    notcats = list(os.listdir(os.path.join("images","not_cat")))
    notcats.sort(reverse=True)

    ## Run predict on all

    c = label_image.ImageClassify()

    def generateImages(limit=10, cats=[], notcats=[]):
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

    for (actuallyCat, src) in generateImages(10000, cats, notcats):
        try:
            _, cat_result, _ = c.predict_image(src)
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

    return generate_roc_data(actuallyCatResults, actuallyNotCatResults)



if __name__ == "__main__":
    sys.exit(main(sys.argv))
