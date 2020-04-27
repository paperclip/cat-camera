#!/bin/env python3
#

import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tensorflow.get_logger().setLevel('ERROR')

GL_CAMERA_DIR = None

def loadModel():
    global GL_CAMERA_DIR
    script_dir = os.path.abspath(os.path.dirname(__file__))
    GL_CAMERA_DIR = os.path.dirname(script_dir)
    if GL_CAMERA_DIR not in sys.path:
        sys.path.append(GL_CAMERA_DIR)
    projects_dir = os.path.dirname(GL_CAMERA_DIR)
    yolo_dir = os.path.join(projects_dir, "tf2-eager-yolo3")
    if yolo_dir not in sys.path:
        sys.path.append(yolo_dir)

    print(yolo_dir)
    os.chdir(yolo_dir)

    import predMulti
    import yolo.config

    config_file = "configs/predict_coco.json"
    config_parser = yolo.config.ConfigParser(config_file)
    model = config_parser.create_model(skip_detect_layer=False)
    detector = config_parser.create_detector(model)
    labels = config_parser.get_labels()

    print(labels)

    return model, detector, labels


def main(argv):
    loadModel()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
