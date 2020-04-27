
import sys

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

def add_yolo3(record):
    updated = database.add_generic_info.add_file_location(record)

    if "yolo3" in record:
        return updated

    image_path = record['current_location']
    result = predict(image_path)

    record['yolo3_cat'] = result.get('cat', 0.0)
    record['yolo3_dog'] = result.get('dog', 0.0)

    record['yolo3'] = max_result(result)

    record.pop("yolo", None)
    record.pop("yolo_cat", None)
    record.pop("yolo_dog", None)

    return True


def add_yolo3_to_all_record(data):
    count = 2000
    for v in data.m_collection:
        if v is None:
            break

        count -= 1
        if count == 0:
            break

        updated = add_yolo3(v)

        if updated:
            print(repr(v))
            data.updateRecord(v)


def main(argv):
    data = database.db.Database()

    try:
        add_yolo3_to_all_record(data)
    finally:
        data.close()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
