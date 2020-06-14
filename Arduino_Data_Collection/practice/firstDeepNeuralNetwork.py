# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 12:55:03 2019

@author: Saurish
"""
# Making neural networks of 4 layers. 
# 8 input features,  10,12,5 hidden units, 1 output unit.

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
df = pd.read_csv('C:\\Users\\Saurish\\Documents\\GitHub\\path_follower_bot\\practice\\Diabetes.csv')
df.classVariable.replace(('YES', 'NO'), (1, 0), inplace=True)
array = df.values
X = array[:,0:8]
Y = array[:,8]

n0 = 8
n1,n2,n3,n4 = 10,12,5,1
#Every Row in weight matrix should represent a node
W1 = np.random.randn(n1,n0) * 0.01 # (10,8)
W2 = np.random.randn(n2,n1) * 0.01 # (12,10)
W3 = np.random.randn(n3,n2) * 0.01 # (5,12)
W4 = np.random.randn(n4,n3) * 0.01 # (1,5)

b1 = np.zeros((n1,1)) #(10,1)
b2 = np.zeros((n2,1)) #(12,1)
b3 = np.zeros((n3,1)) #(5,1)
b4 = np.zeros((n4,1)) #(1,1)

X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state = 3)
Y_train = Y_train.reshape((614,1)).T # (1,m)
X_train = X_train.T #(8,m)
for i in range(1000):
    #Forward Propogation Step.
    Z1 = np.dot(W1,X_train)+b1 #(10,m)
    A1 = 1/(1+np.exp(-1*Z1)) #(10,m)
    Z2 = np.dot(W2,A1) + b2 #(12,m)
    A2 = 1/(1+np.exp(-1*Z2)) #(12,m)
    Z3 = np.dot(W3,A2) + b2 #(12,m)
    A3 = 1/(1+np.exp(-1*Z3)) #(12,m)
    Z4 = np.dot(W4,A3) + b2 #(12,m)
    A4 = 1/(1+np.exp(-1*Z4)) #(12,m)
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
