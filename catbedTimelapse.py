#!/bin/env python
## from 2018-10-21 08:30:09
import os
import sys



import timelapse

def main(argv):
    if len(argv) > 1:
        srcdir = argv[1]
    else:
        srcdir = "cat"

    if len(argv) > 2:
        dest = argv[2]
    else:
        dest = "cat_timelapse.mp4"

    if len(argv) > 3:
        minStem = argv[3]
    else:
        minStem = None

    files = os.listdir(srcdir)

    if minStem is not None:
        files = [ f for f in files if f > minStem ]

    files.sort()

    tempdir = "timelapseTemp"

    i = timelapse.linkIntoTemp(files, srcdir, tempdir, 1000)
    timelapse.createVideo(dest, tempdir, 10)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
