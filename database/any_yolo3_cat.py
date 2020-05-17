#!/bin/env python3

import os
import re
import sys
import time

try:
    from . import db
except ImportError:
    import db


def search_for_yolo(data):
    for v in data.m_collection:
        if v is None:
            break

        yolo3 = v.get("yolo3", None)
        if yolo3 is None:
            continue 

        yolo3_cat = v.get('yolo3_cat', "NOT FOUND")
        if yolo3_cat == "NOT FOUND":
            print(v['name'], "has no yolo3_cat record")
        if yolo3_cat not in (None, 0.0):
            print(v['name'],"yolo3_cat", yolo3_cat)


def main(argv):
    with db.Database() as data:
        search_for_yolo(data)

        for id_value in argv[1:]:
            print(id_value, "=", data.get_record_by_id(int(id_value)))


    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
