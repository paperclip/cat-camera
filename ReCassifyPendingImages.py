#!/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import re

## Reclassify images into the new_cat directory

os.chdir(r"C:\Users\windo\Documents\camera")

import label_image as classifier
c = classifier.ImageClassify()

def newCat():
    for base in range(100,-1,-1):
        directory = os.path.join("new_cat","%02d"%base)
        if not os.path.isdir(directory):
            continue
        pics = os.listdir(directory)
        for p in pics:
            yield os.path.join(directory,p)

def safemkdir(d):
    try:
        os.makedirs(d)
    except EnvironmentError:
        pass

def main(argv):
    pending = list(newCat())
    remaining = len(pending)
    print("Total=",remaining)
    for src in pending:
        try:
            results = c.predict_image(src)
            dest = os.path.join("new_cat","%02d"%(int(results[1][0]*100)))
            safemkdir(dest)
            dest = os.path.join(dest, os.path.basename(src))
            if src != dest:
                print("%s\t%s\t%s\t%d"%(src,str(results),dest,remaining))
                os.rename(src,dest)
            remaining -= 1
        except EnvironmentError as e:
            print("Failed to process %s"%src)
            print(e)
        except Exception as e:
            print("Failed to process %s"%src)
            print(e)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

