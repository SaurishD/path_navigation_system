# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 02:11:58 2019

@author: Saurish
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
import os
import cv2
import sys


miss = 0
def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
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
  sess = tf.Session()
  result = sess.run(normalized)

  return result


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

model_file = \
    "./train_result/output_graph.pb"
label_file = "./train_result/output_labels.txt"
input_height = 160
input_width = 160
input_mean = 0
input_std = 255
input_layer = "input"
output_layer = "final_result"
input_name = "import/" + input_layer
output_name = "import/" + output_layer
graph = load_graph(model_file)
input_operation = graph.get_operation_by_name(input_name)
output_operation = graph.get_operation_by_name(output_name)
read = True
def classify(file_name):
  t = read_tensor_from_image_file(
      file_name,
      input_height=input_height,
      input_width=input_width,
      input_mean=input_mean,
      input_std=input_std)

  results = sess.run(output_operation.outputs[0], {
        input_operation.outputs[0]: t
    })
   
  results = np.squeeze(results)
  
  top_k = results.argsort()[-5:][::-1]
  labels = load_labels(label_file)
  print(labels[top_k[0]])

 

    

if __name__ == "__main__":
    
    in_path = "./videos/right1.mp4"
    if len(sys.argv) == 2:
        in_path = sys.argv[1]
    vid = cv2.VideoCapture(in_path)
    i = 0;
    with tf.Session(graph=graph) as sess:
        while(vid.isOpened()):
            ret, frame = vid.read()
            
            if ret == False:
                break
            if i%5 != 0:
                i = i+1
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray,(300,300))
            frame = cv2.transpose(frame)
            cv2.imshow('Camera Input',cv2.flip(frame,  1))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            cv2.imwrite(os.path.join('./buffer/tmp.jpg'), gray)
            classify('./buffer/tmp.jpg')
            
        vid.release()
        cv2.destroyAllWindows()


