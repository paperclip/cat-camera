#!/bin/env python3

try:
    from . import db
except ImportError:
    import db

data = db.Database()
print(data.m_collection.last_record_id())
data.close()

