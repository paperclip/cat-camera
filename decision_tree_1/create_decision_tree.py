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
    'bird',
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
    'clock',
    'bicycle',
    'truck',
    'book',
    'handbag',
    'suitcase',
    'remote',
    'cell phone',
    'tvmonitor',
    'laptop',
    'backpack',
    'refrigerator',
    None, 
]

GL_YOLO3_REVERSE_CATEGORY_MAP = { v:k for (k,v) in enumerate(GL_YOLO3_CATEGORIES) }

def getFeature(feature, record):
    if feature in (
            'yolo3_cat',
            'yolo3_dog',
            "yolo3_person",
            "yolo3_animal",
            "yolo3_max_value"):
        return record[feature] or 0.0
    elif feature == 'yolo3':
        return GL_YOLO3_REVERSE_CATEGORY_MAP[record[feature]]
    elif feature == 'yolo3_is_animal':
        yolo3 = record['yolo3']
        if yolo3 in ('cat', 'dog', 'bird', 'person'):
            return 1
        return 0
    elif feature == "time":
        return record['hour'] + record['minute'] / 60.0
    elif feature == "weekend":
        wday = record['day_of_week']
        return 1 if wday in (5, 6) else 0

    return record[feature]


def print_decision_tree(data, feature_labels, max_depth=5, min_impurity_decrease=0.005):
    print("Start")
    # print(GL_YOLO3_REVERSE_CATEGORY_MAP)
    result_labels = ["not_cat", "cat"]

    cat_records = []
    not_cat_records = []
    for r in generate_data.generate_records(data):
        if r['cat'] == 1:
            cat_records.append(r)
        else:
            not_cat_records.append(r)

    assert len(cat_records) < len(not_cat_records)

    cr = len(cat_records)
    pos = len(not_cat_records) - cr

    not_cat_records = not_cat_records[pos:]
    assert len(cat_records) == len(not_cat_records)

    X = []
    y = []
    for r in cat_records:
        X.append([getFeature(f, r) for f in feature_labels])
        y.append(r['cat'])
    for r in not_cat_records:
        X.append([getFeature(f, r) for f in feature_labels])
        y.append(r['cat'])

    print("Classify for %d records" % len(X))

    assert len(X) == len(y)

    clf = tree.DecisionTreeClassifier(
        random_state=0, max_depth=max_depth, min_impurity_decrease=min_impurity_decrease)
    clf = clf.fit(X, y)
    text_tree = sklearn.tree.export_text(clf, feature_labels, show_weights=True)
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


def inner_main(data, argv):
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
    feature_labels = ['classify1', 'yolo3_cat', 'size',
                      'time', 'day_of_week', 'yolo3_is_animal', "weekend",
                      "yolo3_person", "yolo3_animal", "yolo3_max_value"]  # , 'yolo3'

    if len(argv) > 1:
        max_depth = int(argv[1])
    else:
        max_depth = 5
    return print_decision_tree(data, feature_labels, max_depth=max_depth,
                               min_impurity_decrease=0.001)

def main(argv):
    with database.db.Database() as data:
        inner_main(data, argv)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
