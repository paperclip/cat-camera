#!/usr/bin/env python3

import os
import sys

def add_camera_dir_to_sys_path():
    GL_DATABASE_SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
    GL_CAMERA_DIR = os.path.dirname(GL_DATABASE_SCRIPT_DIR)

    if GL_CAMERA_DIR not in sys.path:
        sys.path.append(GL_CAMERA_DIR)

add_camera_dir_to_sys_path()

import database.db

def best_classify1(record):
    best_k = 0
    best_v = None

    for (k, v) in record.items():
        if not k.startswith("classify1_"):
            continue
        k = int(k[len("classify1_")+1:])
        if k > best_k:
            best_v = v
    
    if best_v is not None:
        record['classify1'] = best_v


def generate_records(data, count, debug=False):
    """
    Generate count cats and count not_cats which have full details
    """
    REQUIRED_FIELDS = ('cat', 'name', 'yolo3_cat',
                       'yolo3_dog', 'yolo3', 'year', "classify1")
    cat_count = 0
    not_cat_count = 0
    for v in data.m_collection:
        if v is None:
            break

        best_classify1(v)

        usable = True
        for field in REQUIRED_FIELDS:
            if field not in v:
                usable = False
                if debug:
                    print(field,"missing from",v)
                break
        if not usable:
            continue

        if v['cat'] == 1 and cat_count < count:
            cat_count += 1
            yield v
        elif v['cat'] == 0 and not_cat_count < count:
            not_cat_count += 1
            yield v
        
        if cat_count >= count and not_cat_count >= count:
            break




def inner_main(data, count):
    print("Start")
    for record in generate_records(data, count):
        print("USING",record)
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
