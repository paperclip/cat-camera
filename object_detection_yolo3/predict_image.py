

try:
    from . import load_model
except ImportError:
    import load_model

import glob
import cv2
import sys
import os

def predict_image(image_path, detector, class_labels):
    image_path = os.path.join(load_model.GL_CAMERA_DIR, image_path)
    assert os.path.isfile(image_path)

    # 2. Load image
    image = cv2.imread(image_path)
    assert image is not None
    image = image[:, :, ::-1]

    # 3. Run detection
    boxes, labels, probs = detector.detect(image, 0.5)

    # print(list(zip(labels, probs)))

    result = {}
    for (l, p) in zip(labels, probs):
        result[class_labels[l]] = p

    # # 4. draw detected boxes
    # visualize_boxes(image, boxes, labels, probs, config_parser.get_labels())
    #
    # # 5. plot
    # plt.imshow(image)
    # plt.show()
    return result


def main(argv):
    model, detector, class_labels = load_model.loadModel()

    def predict(image_path):
        v = predict_image(image_path, detector, class_labels)
        print(image_path, v)


    for image_path in argv[1:]:
        if "*" in image_path:
            images = glob.glob(image_path)
            for i in images:
                predict(i)
        else:
            predict(image_path)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
