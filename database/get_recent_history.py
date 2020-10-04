#!/bin/env python3

import os
import re
import sys
import time

try:
    from . import db
    from . import add_generic_info
except ImportError:
    import db
    import add_generic_info


def best_classify1(record):
    best_k = 0
    best_v = None

    for (k, v) in record.items():
        if not k.startswith("classify1_"):
            continue
        k = int(k[len("classify1_")+1:])
        if k > best_k:
            best_v = v

    return best_v


def update_is_cat(data, m):
    loc = m['current_location']
    if "images\\not_cat" in loc:
        m['cat'] = False
    elif "images\\cat" in loc:
        m['cat'] = True
    else:
        return False

    print("Converting unknown for",loc,"to",m['cat'])
    return True


def get_recent_history(data, count=1000):
    results = {}
    for m in data.m_collection:
        if m is None:
            break

        count -= 1
        if count == 0:
            break

        if count % 1000 == 0:
            print(count)

        predict_cat = best_classify1(m) >= 50
        actual_cat = m.get('cat', None)
        updated = add_generic_info.add_date_info(m)
        
        if actual_cat is None:
            updated = update_is_cat(data, m) or updated
            actual_cat = m.get('cat', None)

        if updated:
            data.updateRecord(m)

        if actual_cat is None:
            k = 'unknown'
        elif predict_cat:
            if actual_cat:
                k = 'true_positive'
            else:
                k = 'false_positive'
        else:
            if actual_cat:
                k = 'false_negative'
            else:
                k = 'true_negative'


        key = (m.get('year', 2020), m['month'], m['day_of_month'])
        d = results.setdefault(key, {})
        d[k] = d.get(k, 0) + 1

    ret = ['Date,Unknown,TP,FP,FN,TN\n']
    keys = sorted(results.keys())
    for (y, m, d) in keys:
        r = results[(y, m, d)]
        ret.append("%04d-%02d-%02d,%d,%d,%d,%d,%d\n"%(y,m,d,
            r.get('unknown',0),
            r.get('true_positive', 0),
            r.get('false_positive', 0),
            r.get('false_negative', 0),
            r.get('true_negative', 0),
            ))
    return ret

def main(argv):
    start = time.time()
    dest = argv[1]
    if len(argv) > 2:
        count = int(argv[2])
    else:
        count = 5000

    output = open(dest, "w")

    with db.Database() as data:
        results = get_recent_history(data, count)

    end = time.time()
    duration = end - start 
    print("Duration %f (%f/record)", duration, duration / count)

    output.writelines(results)
    output.close()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
