#!/bin/env python
## from 2018-10-21 08:30:09
import os

import timelapse

files = []
tempdir = "catTemp"
srcdir = "cat"

for f in os.listdir(srcdir):
    files.append(f)

files.sort()

i = timelapse.linkIntoTemp(files, srcdir, tempdir, 1000)
timelapse.createVideo("cat_timelapse.mp4", tempdir)
