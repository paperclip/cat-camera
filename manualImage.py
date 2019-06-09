#!/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import re

try:
    import PyQt5.QtCore as QtCore
    from PyQt5.QtWidgets import QApplication
except ImportError:
    try:
        import PyQt4.QtCore as QtCore
        from PyQt4.QtGui import QApplication
    except ImportError:
        raise ImportError("ImageViewerQt: Requires PyQt5 or PyQt4.")

import viewImage

category=[]

os.chdir(r"C:\Users\windo\Documents\camera")

# subprocess.call([RSYNC,"-va","douglas@pi:webdata/camera/","camera"])

#~ cats = set(os.listdir("images/cat"))
#~ notcats = set(os.listdir("images/not_cat"))
#~ camera = set(os.listdir("camera"))

#~ print(len(cats))
#~ print(len(notcats))
#~ print(len(camera))

#~ new = camera - cats
#~ new -= notcats

#~ marker = "timelapse-2018-08-12-13-15-24.jpeg"

def total():
    t = 0
    for base in range(100,-1,-1):
        directory = os.path.join("new_cat","%02d"%base)
        if os.path.isdir(directory):
            pics = os.listdir(directory)
            t += len(pics)
    return t

REMAINING = None

def skipImage(basename):
    if basename > "timelapse-2019-05-04-00" and basename < "timelapse-2019-05-09-00":
        print("Skipping {}".format(basename))
        global REMAINING
        REMAINING -= 1
        return True
    return False

def newCat(imageProcessor):
    for base in range(100,-1,-1):
        directory = os.path.join("new_cat","%02d"%base)
        if not os.path.isdir(directory):
            continue
        pics = os.listdir(directory)
        for p in pics:
            if not skipImage(p):
                yield os.path.join(directory,p)

    imageProcessor.close()

class ManualImageProcessor(object):
    def __init__(self):
        self.m_truePositive = 0
        self.m_trueNegative = 0
        self.m_falsePostive = 0
        self.m_falseNegative = 0
        # Create image viewer and load an image file to display.
        self.m_viewer = viewImage.QtImageViewer()
        self.m_viewer.keyPressed.connect(self.on_key)
        self.m_previousImages = []
        self.m_nextImages = []
        self.m_moreImages = newCat(self)
        self.m_imageName = None
        global REMAINING
        REMAINING = total()
        self.nextImage()
        self.m_viewer.show()

    def close(self):
        print("Killing")
        self.outputCounts()
        self.m_viewer.deleteLater()


    def on_key(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Q:
            self.close()
        elif key == QtCore.Qt.Key_Left:
            return self.previous()
        elif key == QtCore.Qt.Key_Up:
            return self.cat()
        elif key == QtCore.Qt.Key_Right:
            return self.nextImage()
        elif key == QtCore.Qt.Key_Down:
            return self.notcat()

    def previous(self):
        if len(self.m_previousImages) > 0:
            self.m_nextImages.append(self.m_imageName)
            self.setImage(self.m_previousImages.pop())
        else:
            print("No previous image")

    def nextImage(self):
        if self.m_imageName is not None:
            self.m_previousImages.append(self.m_imageName)

        if len(self.m_nextImages) > 0:
            self.setImage(self.m_nextImages.pop())
        else:
            n = next(self.m_moreImages)
            self.setImage(n)

    def cat(self):
        global REMAINING
        print('Cat %d remaining '%REMAINING)
        self.moveImage("images","cat")
        return self.nextImage()

    def notcat(self):
        global REMAINING
        print('Not Cat %d'%REMAINING)
        self.moveImage("images","not_cat")
        return self.nextImage()

    def src(self):
        if os.path.isfile(self.m_imageName):
            return self.m_imageName
        base = os.path.basename(self.m_imageName)
        p = os.path.join("images","not_cat",base)
        if os.path.isfile(p):
            return p
        p = os.path.join("images","cat",base)
        if os.path.isfile(p):
            return p
        return self.m_imageName

    def isPredictedCat(self):
        p = self.m_imageName
        while True:
            p, b = os.path.split(p)
            try:
                return int(b) >= 50
            except ValueError:
                pass
            if b == "":
                break

        return False

    def updateCounts(self, dest):
        predictedCat = self.isPredictedCat()
        actualCat = "not_cat" not in dest
        print("predicted = %r, actual = %r"%(predictedCat,actualCat))

        if predictedCat:
            if actualCat:
                self.m_truePositive += 1
            else:
                self.m_falsePostive += 1
        else:
            if actualCat:
                self.m_falseNegative += 1
            else:
                self.m_trueNegative += 1


    def moveImage(self, *dest):
        base = os.path.basename(self.m_imageName)
        src = self.src()
        dest = os.path.join(*dest, base)
        if src == dest:
            print("%s already moved"%src)
            return

        ## Update counts
        self.updateCounts(dest)
        global REMAINING

        if os.path.isfile(dest):
            print("%s already exists"%dest)
            os.unlink(src)
            REMAINING -= 1
        else:
            print("Rename %s to %s"%(src,dest))
            os.rename(src,dest)
            REMAINING -= 1

    def setImage(self, imageName):
        self.m_imageName = imageName
        src = self.src()
        self.m_viewer.loadImageFromFile(src)

    def outputCounts(self):
        print("True Positive  = %d"%self.m_truePositive)
        print("True Negative  = %d"%self.m_trueNegative)
        print("False Positive = %d"%self.m_falsePostive)
        print("False Negative = %d"%self.m_falseNegative)
        print()
        if self.m_truePositive + self.m_falseNegative > 0:
            print("Recall = %f"% (1.0*self.m_truePositive / (self.m_truePositive + self.m_falseNegative)))
        if self.m_truePositive + self.m_falsePostive > 0:
            print("Precision = %f"%(1.0*self.m_truePositive / (self.m_truePositive + self.m_falsePostive)))
        print()

def main(argv):

    # Create the application.
    app = QApplication(argv)

    processor = ManualImageProcessor()

    # Show viewer and run application.
    try:
        return app.exec_()
    finally:
        processor.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
