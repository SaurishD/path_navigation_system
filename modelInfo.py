# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 20:24:47 2019

@author: Saurish
"""
import tensorflow as tf
def createGraph(modelPath):
    with tf.gfile.FastGFile(modelPath,'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def,name='')

graphDir = r"./train_result./output_graph.pb"
createGraph(graphDir)

for op in tf.get_default_graph().get_operations():
    print(op.values,'\n')