#!/bin/env python

import csv
import os
import re
import sys
import time

dir = "cat"

contents = os.listdir(dir)


## timelapse-2019-08-30-20-19-47.jpeg

# TIMELAPSE_RE = re.compile(r"timelapse-)

lines = []
i = 0

for c in contents:
    tm = time.strptime(c,"timelapse-%Y-%m-%d-%H-%M-%S.jpeg")
    i += 1
    if i % 100 == 0:
        print(c,i)
    if tm.tm_year != 2019:
        continue
    if tm.tm_mon != 8:
        continue

    p = os.path.join(dir, c)
    stat = os.stat(p)
    lines.append((time.strftime("%H:%M:%S",tm), stat.st_size, c))



destpath = "sizes.csv"
with open(destpath, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(lines)
