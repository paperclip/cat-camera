#!/bin/env python3

from unqlite import UnQLite
import os
import sys

GL_DATABASE_SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
GL_CAMERA_DIR = os.path.dirname(GL_DATABASE_SCRIPT_DIR)


## Flags not exposed by python-unqlite
# cdef int UNQLITE_OPEN_READONLY = 0x00000001
# cdef int UNQLITE_OPEN_READWRITE = 0x00000002
# cdef int UNQLITE_OPEN_CREATE = 0x00000004
# cdef int UNQLITE_OPEN_EXCLUSIVE = 0x00000008
# cdef int UNQLITE_OPEN_TEMP_DB = 0x00000010
# cdef int UNQLITE_OPEN_NOMUTEX = 0x00000020
# cdef int UNQLITE_OPEN_OMIT_JOURNALING = 0x00000040
# cdef int UNQLITE_OPEN_IN_MEMORY = 0x00000080
# cdef int UNQLITE_OPEN_MMAP = 0x00000100
UNQLITE_OPEN_READONLY  = 0x00000001
UNQLITE_OPEN_READWRITE = 0x00000002
UNQLITE_OPEN_CREATE    = 0x00000004


class Database(object):
    def __init__(self, write=True):
        camera_dir = GL_CAMERA_DIR
        if write:
            flags = UNQLITE_OPEN_CREATE
        else:
            flags = UNQLITE_OPEN_READONLY
        self.m_db = UnQLite(os.path.join(camera_dir, "cat.unqlite.db"), flags)
        self.m_collection = self.m_db.collection("images")
        self.m_collection.create()
        self.m_slow_lookups = 0
        self.m_quick_lookups = 0
        self.m_new_records = 0
        self.m_writable = write

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
        return False

    def close(self):
        print("Database size = ", self.size())
        print("New records =", self.m_new_records)
        print("Slow lookups =", self.m_slow_lookups)
        print("Quick lookups =", self.m_quick_lookups)
        self.m_db.close()

    def size(self):
        return len(self.m_collection)

    def addValue(self, imageName, key, value, assumeFast=False):
        """
        Combines getRecord and updateRecord for a single value
        """
        return self.getRecord(imageName, key, value, assumeFast=assumeFast)

    def getRecord(self, imageName, key=None, value=None, assumeFast=False):
        """
        Get a record for an imageName, or create it if absent
        """

        if self.m_db.exists(imageName):
            print("Quick lookup",imageName)
            record = self.m_collection[self.m_db[imageName]]
            self.m_quick_lookups += 1
        else:
            # self.debug(imageName)
            if assumeFast:
                records = []
            else:
                records = self.m_collection.filter(
                    lambda record: record['name'] == imageName)
            if len(records) == 0:
                self.m_new_records += 1
                print("New record", imageName)
                record = {'name': imageName}
                if key is not None:
                    record[key] = value
                    key = None
                record_id = self.m_collection.store(record)
                record['__id'] = record_id
            elif len(records) == 1:
                self.m_slow_lookups += 1
                print("Slow lookup", imageName)
                record = records[0]
            else:
                raise KeyError(
                    "%s is recorded in database multiple times: %d" % len(records))

            self.m_db[imageName] = record['__id']

        if key is not None and record.get(key, None) != value:
            record[key] = value
            self.m_collection.update(record['__id'], record)
        return record

    def get_record_by_id(self, id_value):
        return self.m_collection[id_value]

    def updateRecord(self, record):
        self.m_collection.update(record['__id'], record)
        self.m_db[record['name']] = record['__id']
        return record

    def debug(self, imageName):
        print("DB:",len(self.m_db))
        print("Collection:",len(self.m_collection))
        print(imageName in self.m_db)

        n = 5
        for k, v in self.m_db.items():
            if k.startswith("images"):
                continue
            print("Key:",k, v)
            n -= 1
            if n == 0:
                break


