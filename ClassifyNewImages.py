#!/bin/env python

import os
import shutil
import subprocess
import sys

## rsync -va douglas@pi:webdata/camera/ camera

RSYNC=r"F:\cygwin64\bin\rsync"

import tensorflow1.camera_dir
tensorflow1.camera_dir.cd_camera_dir()

# subprocess.call([RSYNC,"-va","douglas@pi:webdata/camera/","camera"])

cameraDir = "cat"
if len(sys.argv) > 1:
    cameraDir = sys.argv[1]
camera = set(os.listdir(cameraDir))


print("Total images %d"%len(camera))
new = camera

for d in os.listdir("images"):
    p = os.path.join("images",d)
    if not os.path.isdir(p):
        continue
    contents = set(os.listdir(p))
    print("%s images %d"%(d,len(contents)))
    new -= contents

def safemkdir(d):
    try:
        os.makedirs(d)
    except EnvironmentError:
        pass

marker = "timelapse-2019-08-01-13-15-24.jpeg"

for i in range(100):
    p = os.path.join("new_cat","%02d"%i)
    try:
        contents = os.listdir(p)
    except EnvironmentError:
        continue
    new -= set(contents)
    old = [ x for x in contents if x < marker ]
    for x in old:
        os.unlink(os.path.join(p,x))


new = [ n for n in new if n > marker ]

new = sorted(new)

print("New images %d"%(len(new)))

import label_image as classifier
c = classifier.ImageClassify()

## ['cat', 'not_cat'], image_size=100, learning_rate=0.001)
## c.load_model('cat_water')

remaining = len(new)

for n in new:
    src = os.path.join(cameraDir,n)
    try:
        stat = os.stat(src)
        if stat.st_size < 100:
            continue
        topLabel, catPercentage, resultMap = c.predict_image(src)
        dest = os.path.join("new_cat","%02d"%(int(catPercentage*100)))
        safemkdir(dest)
        print("%s\t%s\t%f\t%s\t%d\t%s"%(src,topLabel, catPercentage,dest,remaining,str(resultMap)))
        shutil.copy(src,dest)
        remaining -= 1
    except Exception as e:
        print("Failed to process %s"%src)
        print(e)



#~ for n in new:
    #~ src = os.path.join("camera",n)
    #~ dest = os.path.join("not_cat",n)
    #~ shutil.copy(src,dest)
    #~ print(n)
