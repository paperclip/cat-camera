#!/bin/env python

import json
import os
import sys
import numpy as np
from matplotlib import pyplot

def main(argv):
    os.chdir(r"C:\Users\windo\Documents\camera")

    filename = "roc.json"
    if len(argv) > 1:
        filename = argv[1]

    ## list of tuple(false-postive, true-positive)
    results = json.load(open(filename,"r"))

    fpr, tpr = zip(*results)

    pyplot.plot(fpr, tpr)
    pyplot.xlabel("Cat False Positive Rate")
    pyplot.ylabel("Cat True Positive Rate")
    pyplot.title("Cat TensorFlow1 ROC Curve")
    pyplot.show()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
