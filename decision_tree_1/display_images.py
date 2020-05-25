#!/usr/bin/env python

import os
import sys
import time

try:
    from . import generate_data
except ImportError:
    import generate_data

import database.db


def yield_images(data):
    ## classify1 < 17, yolo_cat < 0.25, time > 7.39
    for v in data.m_collection:
        if v is None:
            return
        
        c1 = generate_data.best_classify1(v)

        if c1 is None or c1 > 17:
            continue

        yolo3_cat = v.get('yolo3_cat', None)
        if yolo3_cat is None or yolo3_cat > 0.25:
            continue
            
        if v['hour'] + v['minute'] / 60.0 < 7.39:
            continue

        if "cat" not in v:
            continue

        yield v



def inner_main(data):
    n = 0
    cat = 0
    not_cat = 0
    try:
        for r in yield_images(data):
            print(r['name'])
            n += 1
            if r.get('cat', 0) == 1:
                cat += 1
            else:
                not_cat += 1

            if r['name'] == "timelapse-2019-12-25-08-16-31.jpeg":
                print(r)
    finally:
        print(n, cat, not_cat)
    return 0


def main(argv):
    with database.db.Database() as data:
        return inner_main(data)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
