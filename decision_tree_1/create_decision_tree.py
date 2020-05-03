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
import sklearn.tree
# import sklearn.tree.export

import graphviz

GL_YOLO3_CATEGORIES = [
    "cat",
    "dog",
    'person',
    'bed',
    'sofa',
    'chair',
    'diningtable',
    'sports ball',
    'pottedplant',
    'cup',
    'bowl',
    'bottle',
    'wine glass',
    'vase',
    'bicycle',
    'tvmonitor',
    'laptop',
    'remote',
    'cell phone',
    'backpack',
    'refrigerator',
    None, 
]

GL_YOLO3_REVERSE_CATEGORY_MAP = { v:k for (k,v) in enumerate(GL_YOLO3_CATEGORIES) }

def getFeature(feature, record):
    if feature in (
        'yolo3_cat',
        'yolo3_dog',):
        return record[feature] or 0.0

    if feature == 'yolo3':
        return GL_YOLO3_REVERSE_CATEGORY_MAP[record[feature]]

    return record[feature]


def print_decision_tree(data, count, feature_labels, max_depth=5):
    print("Start")
    # print(GL_YOLO3_REVERSE_CATEGORY_MAP)
    X = []
    y = []
    result_labels = ["not_cat", "cat"]
    clf = tree.DecisionTreeClassifier(random_state=0, max_depth=max_depth)
    for r in generate_data.generate_records(data, count):
        X.append([ getFeature(f, r) for f in feature_labels ])
        y.append(r['cat'])
    # print(X,y)
    if len(X) != 2 * count:
        print("Failed to get enough records")
        print(X, y)
        raise Exception("Failed to get enough records")
    clf = clf.fit(X, y)
    text_tree = sklearn.tree.export_text(clf, feature_labels)
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


def inner_main(data, count):
    # feature_labels = [
    #     'year',
    #     'month',
    #     'day_of_month',
    #     'day_of_week',
    #     'hour',
    #     'minute',
    #     'size',
    #     'yolo3_cat',
    #     'yolo3_dog',
    #     'yolo3',
    #     'classify1',
    # ]
    feature_labels = ['classify1', 'yolo3_cat', 'size', 'hour', 'minute', 'day_of_week']
    return print_decision_tree(data, count, feature_labels)

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
