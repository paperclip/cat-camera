#!/bin/env python3
# 
import tinydb
from unqlite import UnQLite
import os
import sys

def main(argv):
    input_db = tinydb.TinyDB("cat.db.json")
    try:
        os.unlink("cat.unqlite.db")
    except EnvironmentError:
        pass

    output_db = UnQLite("cat.unqlite.db")
    output_collection = output_db.collection("images")
    output_collection.create()
    output_collection.store(input_db.all())


    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
