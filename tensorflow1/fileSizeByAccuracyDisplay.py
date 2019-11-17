#!/bin/env python

import pandas
from matplotlib import pyplot

data = pandas.read_csv("accuracy.csv")

print("FULL DATA:",data)

selector = data['IsCat'] == True
print("SELECTOR:",selector, type(selector))

iscat_data = data[selector]
not_cat_data = data[data['IsCat'] == False]

print("IS_CAT DATA:",iscat_data)
print("NOT CAT DATA:",not_cat_data)

pyplot.plot(iscat_data['Size'], iscat_data['PredictedCat'],
    "ro", label="cat", markersize=4, alpha=0.08)
pyplot.plot(not_cat_data['Size'], not_cat_data['PredictedCat'],
    "bo", label="not cat", markersize=4, alpha=0.08)
pyplot.legend(framealpha=1, markerscale=4.0)
pyplot.xlabel("Size")
pyplot.ylabel("Cat prediction")
pyplot.title("Cat prediction by size")
pyplot.show()
