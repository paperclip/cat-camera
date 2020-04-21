#!/bin/env python

## Delete old pictures from the cat directory
## These have been classified and deleted from the pi, so aren't required any more.

import os
import sys


cameraDir = "cat"
if len(sys.argv) > 1:
    cameraDir = sys.argv[1]
camera = os.listdir(cameraDir)

marker = "timelapse-2019-11"

for f in camera:
    if f < marker:
        print(f)
        os.unlink(os.path.join(cameraDir, f))

print(cameraDir, len(camera), len(os.listdir(cameraDir)))
