#!/usr/bin/python

#this is a script to read in camera data, detect a marshmallow, and read it's toastedness
#toastedness will be done via averaging pixel data of detected marshmallow shape

import cv2
import numpy as np
import imutils

#basic color definitions
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)


#this function detects the presence of a marshmallow
def ShapeDetector(c):
    #base case of no mallow
    status = "No Marshmallow Detected"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, .04*peri, True)

    #detecting if a rectangular shape is found (cross section of marshmallow
    if len(approx) == 4:
        (x,y,w,h) = cv2.boundingRect(approx)
        status = "MARSHMALLOW"
    
    #returning the what an contour is and its bounding box
    return status

def RoastLevel(c):
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, .04*peri, True)
    pass


if __name__ == "__main__":

    #dasic video capture object
    videoCap = cv2.VideoCapture(0)

    #checking successful video capture creation
    if(not videoCap.isOpened()):
        print ("ERROR CANT FIND PI CAMERA")
        quit()
    else:
        print("camera found")


    #reading in a frame
    b, image = videoCap.read()

    #continuously reading in camera data
    while True:

        #reading in a frame
        b, image = videoCap.read()

        #adjusting for more processing
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
            status = ShapeDetector(c)
            if(status == "MARSHMALLOW"):
                #draw name of shape on contour at (x,y) coords
                c = (c.astype("float")*ratio).astype('int')
                cv2.drawContours(image, [c], -1, RED,2)
                cv2.putText(image, status, (c_x,c_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
                #displaying the associated toastedness
                roastLevel = RoastLevel(c)
                cv2.putText(image, roastLevel, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)



        cv2.imshow("Image", image)
        cv2.waitKey(1)
