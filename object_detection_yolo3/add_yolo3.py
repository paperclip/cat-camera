
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
            v = prob
    return r, float(v)

CAT_RESULTS = []


def process_results(record, result):
    global CAT_RESULTS
    cat_result = float(result.get('cat', 0.0))
    record['yolo3_cat'] = cat_result
    if cat_result > 0.0:
        print("***** CAT:", cat_result, record['name'])
        CAT_RESULTS.append(record)
    else:
        # print("no cat:", record['name'])
        pass

    record['yolo3_dog'] = float(result.get('dog', 0.0))
    record['yolo3_person'] = float(result.get('person', 0.0))

    max_animal = 0.0
    for animal in ('cat', 'dog', 'bird', 'person'):
        max_animal = max(max_animal, result.get(animal, 0.0) or 0.0)
    assert max_animal is not None
    record['yolo3_animal'] = float(max_animal)
    assert record['yolo3_animal'] >= record['yolo3_person']
    assert record['yolo3_animal'] >= record['yolo3_dog']
    assert record['yolo3_animal'] >= cat_result

    max_category, max_value = max_result(result)
    record['yolo3'] = max_category
    record['yolo3_max_value'] = max_value or 0.0

    record.pop("yolo", None)
    record.pop("yolo_cat", None)
    record.pop("yolo_dog", None)

    assert record["yolo3_person"] is not None
    assert isinstance(record['yolo3_animal'], float)

    return True


def needs_update(record, force=False):
    if force:
        return True

    if "yolo3" not in record:
        return True

    if record.get("yolo3_cat", None) is None:
        print("%s doesn't contain yolo3_cat" % record['__id'])
        return True

    if record.get("yolo3_animal", None) is None:
        print("%s doesn't contain yolo3_animal: %s" % (record['__id'], repr(record)))
        return True

    if record.get("yolo3_person", None) is None:
        print("%s doesn't contain yolo3_person" % record['__id'])
        return True

    if record.get('yolo3_animal', 0.0) < record.get("yolo3_cat", 0.0):
        print("%s yolo3_animal is less than yolo3_cat" % record['__id'])
        return True


    return False



def add_yolo3(record, force=False):
    if not needs_update(record, force=force):
        return False

    updated = database.add_generic_info.add_file_location(record)

    image_path = record.get('current_location', None)
    if image_path is None:
        print("Can't locate",record['name'])
        return updated

    image_path = os.path.join(database.db.GL_CAMERA_DIR, image_path)
    result = predict(image_path)

    return process_results(record, result)



def add_yolo3_to_all_record(data, max_count=200):
    start = time.time()
    
    commit_count = 0
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
            print(count, repr(v))
            data.updateRecord(v)

            n += 1
            skipped = 0
            count -= 1

            if count == 0:
                break

            commit_count += 1
            if commit_count == 100:
                data.commit()
                commit_count = 0
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
