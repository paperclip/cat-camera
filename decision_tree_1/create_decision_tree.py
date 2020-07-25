#!/usr/bin/env python

import pytz
import datetime
import os
import sys
import time

try:
    from . import generate_data
except ImportError:
    import generate_data

try:
    from . import sun
except ImportError:
    import sun

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

def getTime(record):
    return record['hour'] + record['minute'] / 60.0


SUN = sun.sun(lat=51.6080, long=-1.2448)
TIMEZONE = pytz.timezone("Europe/London")


def get_datetime(record):
    return TIMEZONE.localize(
        datetime.datetime(
            record['year'],
            record['month'],
            record['day_of_month'],
            record['hour'],
            record['minute'],
            record['second'])
    )

def get_sunrise_from_datetime(record_datetime):
    sunrise_time = SUN.sunrise(record_datetime)
    sunrise_datetime = datetime.datetime.combine(record_datetime, sunrise_time)
    return TIMEZONE.localize(sunrise_datetime)

def get_sunrise(record):
    record_datetime = get_datetime(record)
    return get_sunrise_from_datetime(record_datetime)

def get_sunset_from_datetime(record_datetime):
    sunset_time = SUN.sunset(record_datetime)
    sunset_datetime = datetime.datetime.combine(
        record_datetime.date(), sunset_time)
    return TIMEZONE.localize(sunset_datetime)

def get_sunset(record):
    record_datetime = get_datetime(record)
    return get_sunset_from_datetime(record_datetime)

def is_day(record):
    r = get_datetime(record)
    if r.time() < get_sunrise_from_datetime(r).time():
        return 0
    if r.time() < get_sunset_from_datetime(r).time():
        return 1
    return 0

def decimal_time(dt):
    return dt.hour + dt.minute / 60.0

def hours_since_sunrise(record):

    ret = getTime(record) - decimal_time(get_sunrise(record))
    # print(record['hour'], record['minute'], getTime(record), get_sunrise(
    #     record), decimal_time(get_sunrise(record)), ret)
    return ret

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
        return getTime(record)
    elif feature == "weekend":
        wday = record['day_of_week']
        return 1 if wday in (5, 6) else 0
    elif feature == "hours_since_sunrise":
        return hours_since_sunrise(record)
    elif feature == "hours_until_sunset":
        return decimal_time(get_sunset(record)) - getTime(record)
    elif feature == "is_day":
        return is_day(record)

    return record[feature]


def print_decision_tree(data, feature_labels, max_depth=5, min_impurity_decrease=0.005, max_records=0):
    print("Start")
    # print(GL_YOLO3_REVERSE_CATEGORY_MAP)
    result_labels = ["not_cat", "cat"]

    cat_records = []
    not_cat_records = []
    for r in generate_data.generate_records(data):
        if r['cat'] == 1:
            cat_records.append(r)
            if max_records > 0 and len(cat_records) > max_records:
                break
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
                      "yolo3_person", "yolo3_animal", "yolo3_max_value", "is_day",
                      "hours_since_sunrise", "hours_until_sunset"]  # , 'yolo3'

    if len(argv) > 1:
        max_depth = int(argv[1])
    else:
        max_depth = 5

    if len(argv) > 2:
        if argv[2] == "sizetime":
            print("Size-Time tree")
            feature_labels = ['size', 'time', 'day_of_week',
                              "weekend", "is_day", "hours_since_sunrise", "hours_until_sunset"]

    return print_decision_tree(data, feature_labels, max_depth=max_depth,
                               min_impurity_decrease=0.001, max_records=0)

def main(argv):
    with database.db.Database() as data:
        inner_main(data, argv)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
