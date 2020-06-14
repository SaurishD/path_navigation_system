# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 13:50:51 2019

@author: Saurish
"""

import serial
import cv2
import os
ser = None
cam = cv2.VideoCapture(1)
path = "./Images/"
file = open("data.csv", "w")
if not os.path.isdir(path):
    os.mkdir(path) 

i = 0

while ser == None:
    try:
        ser = serial.Serial('COM5', 115200)
    except:
        print('please reconnect arduino')

gather = 0
while True:
    
    #Read from serial port
    line = ser.readline()
    if line=='':
        continue
    
    line = str(line)
    line = line.replace("'",'')
    line = line.replace("b",'')
    line = line.replace('\\r\\n','')
    print(line)
    if line=='':
        continue
    if(line == "A"):
        gather = 1
        continue
    
    if(line == "B"):
        gather = 0
        continue
    
    if gather == 0:
        continue
    
    ret, frame = cam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame,(300,300))
    cv2.imwrite(os.path.join(path , str(i)+'.jpg'), frame)
    file.write(line+","+path+str(i)+'.jpg,'+'\n')
    cv2.imshow('image',frame)
    i = i + 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

file.close()