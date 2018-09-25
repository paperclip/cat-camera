#!/usr/bin/env python

import glob
import os
import random

cat_images = glob.glob('cat/*.jpeg')
assert(len(cat_images) > 10)

not_cat_images = glob.glob('not_cat/*.jpeg')
assert(len(not_cat_images) > 10)

selected_not_cat_images = [ x for x in not_cat_images if os.path.getsize(x) > 80 * 1024 ]
selected_not_cat_images = random.sample(selected_not_cat_images, len(cat_images) * 1)

images = cat_images + selected_not_cat_images

assert(len(images) == 2 * len(cat_images))

print("%d cat images"%len(cat_images))
print("%d not_cat images"%len(selected_not_cat_images))


import image_classify
c = image_classify.ImageClassify(['cat', 'not_cat'], image_size=100, learning_rate=0.001)
c.prepare_data(images)
c.train_model('cat_water')
