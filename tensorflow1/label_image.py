# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

import os
import numpy as np
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, "rb") as f:
      graph_def.ParseFromString(f.read())
    with graph.as_default():
      tf.import_graph_def(graph_def)

    graph.finalize()

    return graph


def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255,
                                sess=None):
    input_name = "file_reader"
    output_name = "normalized"
    with tf.Graph().as_default(), tf.Session() as sess:
        file_reader = tf.read_file(file_name, input_name)
        if file_name.endswith(".png"):
            image_reader = tf.image.decode_png(
                file_reader, channels=3, name="png_reader")
        elif file_name.endswith(".gif"):
            image_reader = tf.squeeze(
                tf.image.decode_gif(file_reader, name="gif_reader"))
        elif file_name.endswith(".bmp"):
            image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
        else:
            image_reader = tf.image.decode_jpeg(
                file_reader, channels=3, name="jpeg_reader")
        float_caster = tf.cast(image_reader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0)
        resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])

        #~ if sess is None:
            #~ with tf.Session() as sess:
                #~ result = sess.run(normalized)
        #~ else:
        result = sess.run(normalized)

    return result


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

class ImageClassify(object):
    def __init__(self):
        model_file = \
        "cat_retrained.pb"
        label_file = "cat_labels.txt"
        self.m_input_height = 299
        self.m_input_width = 299
        self.m_input_mean = 0
        self.m_input_std = 255
        self.m_input_layer = "Placeholder"
        self.m_output_layer = "final_result"
        self.m_graph = load_graph(model_file)
        input_name = "import/" + self.m_input_layer
        output_name = "import/" + self.m_output_layer
        self.m_input_operation = self.m_graph.get_operation_by_name(input_name)
        self.m_output_operation = self.m_graph.get_operation_by_name(output_name)
        self.m_labels = load_labels(label_file)
        self.m_session = tf.Session(graph=self.m_graph)
        self.m_loadSession = tf.Session()
        self.m_count = 0

    def predict_image(self, file_name):
        t = read_tensor_from_image_file(
          file_name,
          input_height=self.m_input_height,
          input_width=self.m_input_width,
          input_mean=self.m_input_mean,
          input_std=self.m_input_std,
          sess=self.m_loadSession)

        #~ if self.m_count % 100 == 0:
            #~ self.m_session = tf.Session(graph=self.m_graph)

        if self.m_session is None:
            with tf.Session(graph=self.m_graph) as sess:
                results = sess.run(self.m_output_operation.outputs[0], {
                    self.m_input_operation.outputs[0]: t
                })
        else:
            results = self.m_session.run(self.m_output_operation.outputs[0], {
                self.m_input_operation.outputs[0]: t
            })

        ## Remove single-dimensional entries from the shape of an array.
        results = np.squeeze(results)

        ## Returns the indices that would sort an array.
        ## Then get the last 5, then reverse
        top_k = results.argsort()[-5:][::-1]
        labels = self.m_labels
        resultMap = {}
        for i in top_k:
            resultMap[labels[i]] = results[i]

        self.m_count += 1

        return labels[top_k[0]],results[labels.index('cat')],resultMap

if __name__ == "__main__":
  file_name = "tensorflow/examples/label_image/data/grace_hopper.jpg"
  model_file = \
    "cat_retrained.pb"
  label_file = "cat_labels.txt"
  input_height = 299
  input_width = 299
  input_mean = 0
  input_std = 255
  input_layer = "Placeholder"
  output_layer = "final_result"

  parser = argparse.ArgumentParser()
  parser.add_argument("--image", help="image to be processed")
  parser.add_argument("--graph", help="graph/model to be executed")
  parser.add_argument("--labels", help="name of file containing labels")
  parser.add_argument("--input_height", type=int, help="input height")
  parser.add_argument("--input_width", type=int, help="input width")
  parser.add_argument("--input_mean", type=int, help="input mean")
  parser.add_argument("--input_std", type=int, help="input std")
  parser.add_argument("--input_layer", help="name of input layer")
  parser.add_argument("--output_layer", help="name of output layer")
  args = parser.parse_args()

  if args.graph:
    model_file = args.graph
  if args.image:
    file_name = args.image
  if args.labels:
    label_file = args.labels
  if args.input_height:
    input_height = args.input_height
  if args.input_width:
    input_width = args.input_width
  if args.input_mean:
    input_mean = args.input_mean
  if args.input_std:
    input_std = args.input_std
  if args.input_layer:
    input_layer = args.input_layer
  if args.output_layer:
    output_layer = args.output_layer

  graph = load_graph(model_file)
  t = read_tensor_from_image_file(
      file_name,
      input_height=input_height,
      input_width=input_width,
      input_mean=input_mean,
      input_std=input_std)

  input_name = "import/" + input_layer
  output_name = "import/" + output_layer
  input_operation = graph.get_operation_by_name(input_name)
  output_operation = graph.get_operation_by_name(output_name)

  with tf.Session(graph=graph, config=tf.ConfigProto(log_device_placement=True)) as sess:
    results = sess.run(output_operation.outputs[0], {
        input_operation.outputs[0]: t
    })
  results = np.squeeze(results)

  top_k = results.argsort()[-5:][::-1]
  labels = load_labels(label_file)
  for i in top_k:
    print(labels[i], results[i])
