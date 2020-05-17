#!/bin/env python3

import os
import sys

sys.path.append(os.getcwd())


try:
    from . import add_yolo3
except ImportError:
    import add_yolo3

print(sys.path)
import database.db


def inner_main(data, argv):
    for id_value in argv[1:]:
        print(id_value)
        record = data.get_record_by_id(id_value)
        print("BEFORE:", record)
        record.pop("yolo3", None)
        record.pop("yolo3_cat", None)
        record['test_float'] = 0.5
        data.updateRecord(record)
        print("2:", record)
        record = data.get_record_by_id(id_value)
        print("3:", record)
        updated = add_yolo3.add_yolo3(record, True)
        yolo3_cat = record['yolo3_cat']
        assert yolo3_cat is not None
        print("AFTER:", updated, record, type(yolo3_cat))
        record['test_float'] = 0.6
        data.updateRecord(record)
        record = data.get_record_by_id(id_value)
        print("RELOAD:", record)
        record['yolo3_cat'] = yolo3_cat
        record['test_float'] = 0.7
        data.m_collection.update(record['__id'], record)
        record = data.m_collection[record['__id']]
        print("RELOAD2:", record)
    return 0

def main(argv):
    with database.db.Database() as data:
        return inner_main(data, argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
