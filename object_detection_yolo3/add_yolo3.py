
import os
import sys
import time

try:
    from . import predict_image
    from . import load_model
except ImportError:
    import predict_image
    import load_model

model, detector, class_labels = load_model.loadModel()

import database.db
import database.add_generic_info


def predict(image_path):
    return predict_image.predict_image(image_path, detector, class_labels)


def max_result(result):
    r = None
    v = 0.0

    for result, prob in result.items():
        if prob > v:
            r = result
    return r

CAT_RESULTS = []

def add_yolo3(record, force=False):
    global CAT_RESULTS

    if force is False:
        if "yolo3" in record and record.get("yolo3_cat") is not None:
            return False

    updated = database.add_generic_info.add_file_location(record)

    image_path = record.get('current_location', None)
    if image_path is None:
        print("Can't locate",record['name'])
        return updated

    image_path = os.path.join(database.db.GL_CAMERA_DIR, image_path)
    result = predict(image_path)

    cat_result = float(result.get('cat', 0.0))
    record['yolo3_cat'] = cat_result
    record['yolo3_dog'] = float(result.get('dog', 0.0))

    if cat_result > 0.0:
        print("***** CAT:",cat_result,record['name'])
        CAT_RESULTS.append(record)
    else:
        print("no cat:",record['name'])

    record['yolo3'] = max_result(result)

    record.pop("yolo", None)
    record.pop("yolo_cat", None)
    record.pop("yolo_dog", None)

    return True


def add_yolo3_to_all_record(data, max_count=200):
    start = time.time()
    
    n = 0
    skipped = 0
    count = max_count
    for v in data.m_collection:
        if v is None:
            break

        updated = add_yolo3(v)

        if updated:
            if skipped > 0:
                print("Skipped",skipped)
            print(repr(v))
            data.updateRecord(v)

            n += 1
            skipped = 0
            count -= 1
            if count == 0:
                break
        else:
            skipped += 1

    end = time.time()
    print("Updated %d records in %f seconds" % (n, end - start))


def main(argv):
    max_count = 200
    if len(argv) > 1:
        max_count = int(argv[1])

    with database.db.Database() as data:
        add_yolo3_to_all_record(data, max_count)

    for c in CAT_RESULTS:
        print(repr(c))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
