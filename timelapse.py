#!/bin/env python
## from 2018-10-21 08:30:09
import os
import subprocess
import sys

def clearTemp(tempdir):
    try:
        os.mkdir(tempdir)
    except EnvironmentError:
        pass

    for f in os.listdir(tempdir):
        os.unlink(os.path.join(tempdir,f))

def deleteFile(f):
    try:
        os.unlink(f)
    except EnvironmentError:
        pass

def linkIntoTemp(fileList, srcdir, tempdir, minSize=1000):
    clearTemp(tempdir)
    i = 0
    for f in fileList:
        src=os.path.join(srcdir,f)
        statbuf = os.stat(src)
        if statbuf.st_size < minSize:
            continue
        dest = os.path.join(tempdir,"image%05d.jpeg"%i)
        os.link(src,dest)
        i += 1
    return i

def createVideo(destFileName, tempdir, fps=20):
    """Create a video from the tempdir created by linkIntoTemp"""
    deleteFile(destFileName)
    subprocess.call(['ffmpeg','-r',str(fps),
        '-i',os.path.join(tempdir,"image%05d.jpeg"),
        destFileName])
    return 0

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

    i = linkIntoTemp(files, srcdir, tempdir, 1000)
    return createVideo(dest, tempdir, 10)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
