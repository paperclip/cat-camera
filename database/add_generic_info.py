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
    camera_dir = db.GL_CAMERA_DIR
    if "name" not in m:
        print("Invalid entry?", repr(m))
        return False

    p = m.get('current_location', None)
    if p is not None and os.path.isfile(p):
        return False

    filename = m['name']

    def try_dir(p):
        if os.path.isfile(os.path.join(camera_dir, p)):
            m['current_location'] = p
            return True
        return False

    if (
        try_dir(os.path.join("images", "cat", filename)) or
        try_dir(os.path.join("images", "not_cat", filename))
        ):
        return True

    for i in range(100):
        if try_dir(os.path.join("new_cat", "%02d"%i, filename)):
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
    start = time.time()
    n = 0 
    for v in data.m_collection:
        if v is None:
            break
        updated = add_date_info(v) 
        updated = add_file_location(v) or updated
        updated = add_file_size(v) or updated
        if updated:
            print(repr(v))
            data.updateRecord(v)
            n += 1
    end = time.time()
    print("End: Updated %d records in %f seconds" % (n, end - start))


def main(argv):
    with db.Database() as data:
        add_generic_info(data)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
