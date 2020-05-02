#!/usr/bin/env python

import os
import sys
import time

try:
    from . import generate_data
except ImportError:
    import generate_data

import database.db

from sklearn import tree
import sklearn.tree.export

import graphviz

GL_YOLO3_CATEGORIES = [
    "cat",
    "dog",
    'sports ball',
    'chair',
    'pottedplant',
    'tvmonitor',
    'person',
    'remote',
    'bowl',
    'vase',
    'bottle',
    'bicycle',
    'cell phone',

    None,
]

GL_YOLO3_REVERSE_CATEGORY_MAP = { v:k for (k,v) in enumerate(GL_YOLO3_CATEGORIES) }

def inner_main(data, count):
    print("Start")
    # print(GL_YOLO3_REVERSE_CATEGORY_MAP)
    X = []
    y = []
    result_labels = ["not_cat", "cat"]
    feature_labels = [
        'year',
        'month',
        'day_of_month',
        'day_of_week',
        'hour',
        'minute',
        'size',
        'yolo3_cat',
        'yolo3_dog',
        'yolo3',
        'classify1',
    ]
    clf = tree.DecisionTreeClassifier(random_state=0, max_depth=5)
    for r in generate_data.generate_records(data, count):
        X.append([
            r['year'],
            r['month'],
            r['day_of_month'],
            r['day_of_week'],
            r['hour'],
            r['minute'],
            r['size'],
            r['yolo3_cat'] or 0.0,
            r['yolo3_dog'] or 0.0,
            GL_YOLO3_REVERSE_CATEGORY_MAP[r['yolo3']],
            r['classify1'],
        ])
        y.append(r['cat'])
    print(X,y)
    clf = clf.fit(X, y)
    text_tree = sklearn.tree.export.export_text(clf, feature_labels)
    print(text_tree)
    tree.plot_tree(clf)
    tree.export_graphviz(clf, out_file="cat-decision-tree.dot",
                                    feature_names=feature_labels,
                                    class_names=result_labels,
                                    filled=True, rounded=True,
                                    special_characters=True)
    # graph = graphviz.Source(dot_data)
    # graph.render("cat-decision-tree.gv", view=True, format='svg')
    # graph.view()
    print("End")


def main(argv):
    count = 10
    if len(argv) > 1:
        count = int(argv[1])
    data = database.db.Database()
    try:
        inner_main(data, count)
    finally:
        data.close()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
