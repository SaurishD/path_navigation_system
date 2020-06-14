# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 12:55:03 2019

@author: Saurish
"""
#Making neural networks of 1 hidden layer. 
# 8 input features,  10 hidden units, 1 output units.

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
df = pd.read_csv('C:\\Users\\Saurish\\Documents\\GitHub\\path_follower_bot\\practice\\Diabetes.csv')
df.classVariable.replace(('YES', 'NO'), (1, 0), inplace=True)
array = df.values
X = array[:,0:8]
Y = array[:,8]
W1 = np.random.randn((10,8)) * 0.01 #Every Row in weight matrix should represent a node
W2 = np.random.randn((1,10)) * 0.01
b1 = np.zeros((10,1))
b2 = np.zeros((1,1))
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state = 3)
Y_train = Y_train.reshape((614,1)).T
X_train = X_train.T
for i in range(1000):
    #Forward Propogation Step.
    Z1 = np.dot(W1.T,X_train)+b1.T
    A1 = 1/(1+np.exp(Z1))
    Z2 = np.dot(W2.T,A1) + b2
    A2 = 1/(1+np.exp(Z2))
    #Backward Propogation Step
    dZ2 = (A2-Y_train)
    dW2 = np.dot(dZ2 , A1.T) / 614
    db2 = np.sum(dZ2,axis = 1,keepdims = True) / 614
    dZ1 = np.dot(W2,dZ2)*(A1*(1-A1))
    dW1 = np.dot(X_train,dZ1.T)/614
    db1 = np.sum(dZ1,axis = 1,keepdims = True) / 614
    learning_rate = 20
    W2 = W2 - learning_rate * dW2 
    b2 = b2 - learning_rate * db2
    W1 = W1 - learning_rate * dW1 
    b1 = b1 - learning_rate * db1
