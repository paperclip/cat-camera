#!/bin/env python
## from 2018-10-21 08:30:09
import os
import time

base = "timelapse-2018-10-21-08-30-09.jpeg"
files = []
weekend = []
conservatoryTemp = "conservatoryTemp"

for f in os.listdir("conservatory"):
    if f < base:
        continue
    timestruct = time.strptime(f,"timelapse-%Y-%m-%d-%H-%M-%S.jpeg")
    if timestruct.tm_hour < 8:
        continue
    if timestruct.tm_hour > 17:
        continue

    if timestruct.tm_wday >= 5:
        weekend.append(f)
    else:
        files.append(f)

weekend.sort()
files.sort()

def clearTemp():
    try:
        os.mkdir(conservatoryTemp)
    except EnvironmentError:
        pass

    for f in os.listdir(conservatoryTemp):
        os.unlink(os.path.join(conservatoryTemp,f))

def linkIntoTemp(fileList):
    clearTemp()
    i = 0
    for f in fileList:
        src=os.path.join("conservatory",f)
        statbuf = os.stat(src)
        if statbuf.st_size < 1000:
            continue
        dest = os.path.join(conservatoryTemp,"image%05d.jpeg"%i)
        os.link(src,dest)
        i += 1
    return i

def deleteFile(f):
    try:
        os.unlink(f)
    except EnvironmentError:
        pass

import subprocess

LAST=500

i = linkIntoTemp(weekend)
deleteFile("conservatory_weekend.mp4")
subprocess.call(['ffmpeg','-r','8',
    "-start_number",str(i-LAST),
    '-i',os.path.join(conservatoryTemp,"image%05d.jpeg"),
    "conservatory_weekend.mp4"])

i = linkIntoTemp(files)
deleteFile("conservatory_timelapse.mp4")
subprocess.call(['ffmpeg','-r','30',
    '-i',os.path.join(conservatoryTemp,"image%05d.jpeg"),
    "conservatory_timelapse.mp4"])

if i>LAST:
    deleteFile("conservatory_timelapse_last_day.mp4")
    command = ['ffmpeg','-r','8',
        "-start_number",str(i-LAST),
        '-i',os.path.join(conservatoryTemp,"image%05d.jpeg"),
        "conservatory_timelapse_last_day.mp4"]
    print("Running %s"%str(command))
    subprocess.call(command)
