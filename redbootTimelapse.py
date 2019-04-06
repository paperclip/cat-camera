#!/bin/env python
## from 2018-10-21 08:30:09
import os

import timelapse

files = []
tempdir = "redbootTemp"
srcdir = "redboot"

for f in os.listdir(srcdir):
    files.append(f)

files.sort()

i = timelapse.linkIntoTemp(files, srcdir, tempdir, 1000)
timelapse.createVideo("redboot_timelapse.mp4", tempdir)
