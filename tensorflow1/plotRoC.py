#!/bin/env python

import json
import os
import sys
import numpy as np
from matplotlib import pyplot
import matplotlib.lines as lines

try:
    import camera_dir
except ImportError:
    from . import camera_dir

def main(argv):
    camera_dir.cd_camera_dir()

    filename = "roc.json"
    if len(argv) > 1:
        filename = argv[1]

    ## list of tuple(false-postive, true-positive)
    results = json.load(open(filename,"r"))

    fpr, tpr = zip(*results)

    pyplot.plot(fpr, tpr)
    pyplot.plot([0,1],[0,1], "k-", lw=1, dashes=[2,2])
    pyplot.xlabel("Cat False Positive Rate")
    pyplot.ylabel("Cat True Positive Rate")
    pyplot.title("Cat TensorFlow1 ROC Curve")
    pyplot.show()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
