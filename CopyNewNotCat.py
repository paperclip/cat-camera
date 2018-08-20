#!/bin/env python

import os
import shutil

cats = set(os.listdir("cat"))
notcats = set(os.listdir("not_cat"))
camera = set(os.listdir("camera"))

print(len(cats))
print(len(notcats))
print(len(camera))

new = camera - cats
new -= notcats

marker = "timelapse-2018-08-12-13-15-24.jpeg"

new = [ n for n in new if n > marker ]

new = sorted(new)

for n in new:
    src = os.path.join("camera",n)
    dest = os.path.join("not_cat",n)
    shutil.copy(src,dest)
    print(n)
    

