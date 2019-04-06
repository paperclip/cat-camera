#!/bin/env python
## from 2018-10-21 08:30:09
import os

import timelapse

base = "timelapse-2019-01-13-16-25-47.jpeg"
files = []
tempdir = "catTemp"
srcdir = "cat"

for f in os.listdir(srcdir):
    if f < base:
        continue
    files.append(f)

files.sort()

#~ i = timelapse.linkIntoTemp(files, srcdir, tempdir, 1000)
#~ timelapse.createVideo("hall_timelapse.mp4", tempdir)

files = files[-24*60:]
i = timelapse.linkIntoTemp(files, srcdir, tempdir, 1000)
timelapse.createVideo("hall_timelapse_recent.mp4", tempdir, 10)
