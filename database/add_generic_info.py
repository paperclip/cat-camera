#!/bin/env python3

import os
import re
import sys
import time

try:
    from . import db
except ImportError:
    import db


def add_date_info(m):
    if m is None:
        return False
    if "second" in m:
        return False
    if "name" not in m:
        print("Invalid entry?", repr(m))
        return False
    filename = m['name']
    output = time.strptime(filename, "timelapse-%Y-%m-%d-%H-%M-%S.jpeg")
    if output is None:
        print("Bad filename? ", filename)
    m['year'] = output.tm_year
    m['month'] = output.tm_mon
    m['day_of_month'] = output.tm_mday
    m['day_of_week'] = output.tm_wday
    m['hour'] = output.tm_hour
    m['minute'] = output.tm_min
    m['second'] = output.tm_sec
    return True


def add_file_location(m):
    if "name" not in m:
        print("Invalid entry?", repr(m))
        return False

    p = m.get('current_location', None)
    if p is not None and os.path.isfile(p):
        return False

    filename = m['name']

    p = os.path.join("images", "cat", filename)
    if os.path.isfile(p):
        m['current_location'] = p
        return True

    p = os.path.join("images", "not_cat", filename)
    if os.path.isfile(p):
        m['current_location'] = p
        return True

    for i in range(100):
        p = os.path.join("new_cat", "%2d"%i, filename)
        if os.path.isfile(p):
            m['current_location'] = p
            return True

    return False


def add_file_size(m):
    if "size" in m:
        return False
    p = m.get('current_location', None)
    if p is not None and os.path.isfile(p):
        statbuf = os.stat(p)
        m['size'] = statbuf.st_size
        return True
    return False


def add_generic_info(data):
    print("Start")
    for v in data.m_collection:
        if v is None:
            break
        updated = add_date_info(v) 
        updated = add_file_location(v) or updated
        updated = add_file_size(v) or updated
        if updated:
            print(repr(v))
            data.updateRecord(v)
    print("End")


def main(argv):
    data = db.Database()
    try:
        add_generic_info(data)
    finally:
        data.close()

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
