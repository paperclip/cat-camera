#!/bin/env python

import os
import shutil
import subprocess

## rsync -va douglas@pi:webdata/camera/ camera

RSYNC=r"F:\cygwin64\bin\rsync"

os.chdir(r"C:\Users\windo\Documents\camera")

# subprocess.call([RSYNC,"-va","douglas@pi:webdata/camera/","camera"])

catDir = os.path.join("images","cat")

cats = set(os.listdir(catDir))
notcats = set(os.listdir(os.path.join("images","not_cat")))
camera = set(os.listdir("camera"))

assert len(cats) > 0
assert len(notcats) > 0

print("Cat images %d"%len(cats))
print("Not cat images %d"%len(notcats))
print("Total images %d"%len(camera))

new = camera - cats
new -= notcats

def safemkdir(d):
    try:
        os.makedirs(d)
    except EnvironmentError:
        pass

for i in range(10):
    p = os.path.join("new_cat","%d0"%i)
    safemkdir(p)
    new -= set(os.listdir(p))

marker = "timelapse-2018-08-12-13-15-24.jpeg"

new = [ n for n in new if n > marker ]

new = sorted(new)

print("New images %d"%(len(new)))

import label_image as classifier
c = classifier.ImageClassify()

## ['cat', 'not_cat'], image_size=100, learning_rate=0.001)
## c.load_model('cat_water')

remaining = len(new)

for n in new:
    src = os.path.join("camera",n)
    results = c.predict_image(src)
    dest = os.path.join("new_cat","%d0"%(int(results[1][0]*10)))
    print("%s\t%s\t%s\t%d"%(src,str(results),dest,remaining))
    shutil.copy(src,dest)
    remaining -= 1



#~ for n in new:
    #~ src = os.path.join("camera",n)
    #~ dest = os.path.join("not_cat",n)
    #~ shutil.copy(src,dest)
    #~ print(n)


