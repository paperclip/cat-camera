#!/bin/env python

import os
import shutil
import subprocess

RSYNC=r"F:\cygwin64\bin\rsync"

os.chdir(r"C:\Users\windo\Documents\camera")

# subprocess.call([RSYNC,"-va","douglas@pi:webdata/camera/","camera"])

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

def safemkdir(d):
    try:
        os.makedirs(d)
    except EnvironmentError:
        pass

for i in range(10):
    safemkdir("new_cat/%d0"%i)


import image_classify
c = image_classify.ImageClassify(['cat', 'not_cat'], image_size=100, learning_rate=0.001)
c.load_model('cat_water')

print(len(new))

for n in new:
    src = os.path.join("camera",n)
    results = c.predict_image(src)
    dest = os.path.join("new_cat","%d0"%(int(results[1][0]*10)))
    print(src,results,dest)
    shutil.copy(src,dest)



#~ for n in new:
    #~ src = os.path.join("camera",n)
    #~ dest = os.path.join("not_cat",n)
    #~ shutil.copy(src,dest)
    #~ print(n)


