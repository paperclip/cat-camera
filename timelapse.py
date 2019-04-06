#!/bin/env python
## from 2018-10-21 08:30:09
import os
import subprocess

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
