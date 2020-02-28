#!/usr/bin/python

#this is a script to read in camera data and then detect 
#a rectangle or not

import cv2
import numpy as np
import imutils



def ShapeDetector(c):
    shape = "not rectangle"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, .04*peri, True)

    if len(approx) == 4:
        (x,y,w,h) = cv2.boundingRect(approx)
        shape = "RECTANGLE"
    
    return shape



if __name__ == "__main__":

    #dasic video capture object
    videoCap = cv2.VideoCapture(0)

    #checking successful video capture creation
    if(not videoCap.isOpened()):
        print ("ERROR CANT FIND PI CAMERA")
        quit()
    else:
        print("camera found")

    #continuously reading in camera data
    while True:
        #reading in a frame
        b, image = videoCap.read()

        #loading the frame for more processing
        #image = cv2.imread(frame)
        im_resize = imutils.resize(image, width=300)
        ratio = image.shape[0]/float(im_resize.shape[0])
    
        #image processing steps
        gray = cv2.cvtColor(im_resize, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5,5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

        #contour finding and rectangle identification
        conts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        conts = imutils.grab_contours(conts)
        

        #find shapes based on contours
        for c in conts:
            #finding the center of the contour using moments
            M=cv2.moments(c)
            c_x = 75#int((M["m10"]/M["m00"])*ratio)
            c_y = 75#int((M["m01"]/M["m00"])*ratio)
            shape = ShapeDetector(c)
            if(shape == "RECTANGLE"):
                #draw name of shape on contour at (x,y) coords
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                cv2.drawContours(image, [c], -1, (0,255,0),2)
                cv2.putText(image, shape, (c_x,c_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)


        cv2.imshow("Image", image)
        cv2.waitKey(1)
