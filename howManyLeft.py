#!/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

for base in range(9,-1,-1):
    directory = os.path.join("new_cat","%d0"%base)
    pics = os.listdir(directory)
    print(directory,len(pics))


