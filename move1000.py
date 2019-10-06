#!/bin/env python

import os
import sys

imagesdir = "images"
catdir = os.path.join(imagesdir, "cat")
destdir = os.path.join(imagesdir, "cat1000")

files = os.listdir(catdir)
files.sort()

files = files[:1000]
assert len(files) == 1000

for f in files:
    src = os.path.join(catdir, f)
    dest = os.path.join(destdir, f)
    os.rename(src, dest)
    print(src, dest)
    
