#!/bin/env python

import os
import sys

imagesdir = "images"
catdir = os.path.join(imagesdir, "not_cat")
destdir = os.path.join(imagesdir, "1000")

files = os.listdir(catdir)
files.sort()

files = files[:1000]
assert len(files) == 1000

try:
    os.makedirs(destdir)
except EnvironmentError:
    pass

for f in files:
    src = os.path.join(catdir, f)
    dest = os.path.join(destdir, f)
    os.rename(src, dest)
    print(src, dest)
