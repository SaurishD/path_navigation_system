# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 20:03:28 2019

@author: Saurish
"""

import cv2
import os
i = 0
def video(name,path,skip,start):
    print(name)
    global i
    vid = cv2.VideoCapture(name)
    while(vid.isOpened()):
        ret, frame = vid.read()
        if i%skip != 0 or i<start:
            i = i + 1
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame,(300,300))
        cv2.imwrite(os.path.join(path , str(i)+'_v.jpg'), frame)
        cv2.imshow('frame',frame)
        i = i+1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

path = './videos/'
i = 0
for j in range(1,7):
    try:
        video(path+'straight'+str(j)+'.mp4',path+'straight/',20,200)
    except:
        pass
i = 0
for j in range(1,3):
    try:
        video(path+'left'+str(j)+'.mp4',path+'left/',1,0)
    except:
        pass
i = 0
for j in range(1,4):
    try:
        video(path+'right'+str(j)+'.mp4',path+'right/',1,0)
    except:
        pass
i = 0
try:
    video(path+'stop'+'.mp4',path+'stop/',1,0)
except:
    pass