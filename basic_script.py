#!/usr/bin/python

#this is a basic script found on stack overflow from link on 5725 website


import cv2
import numpy as np

#dasic video capture object
videoCap = cv2.VideoCapture(0)

#checking successful video capture creation
if(not videoCap.isOpened()):
    print ("ERROR CANT FIND PI CAMERA")
    quit()
else:
    print("camera found")


while True:
    b, frame = videoCap.read()
    cv2.imshow("frame", frame)
    cv2.waitKey(1)
