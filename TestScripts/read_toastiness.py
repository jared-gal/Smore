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
    approx = cv2.approxPolyDP(c, .1*peri, True)

    #detecting if a rectangular shape is found (cross section of marshmallow
    if len(approx) == 4:
        (x,y,w,h) = cv2.boundingRect(approx)
        status = "MARSHMALLOW"
    
    #returning the contour status as potential mallow or not
    return status

#this function takes in a grayscale image and a given contour to find
#the darkening of the specific region bound by the contour
def RoastLevel(c,img):

    #finding the pixels in a given contour and creating a mask of those pixels
    mask = np.zeros_like(img)
    cv2.drawContours(mask, c,-1, color=255,thickness =-1)

    #recording the pixels on the interior of the mask
    pixs = np.where(mask==255)

    #initialize several useful variables
    pix_dark = 0    #total darkness value of the region
    count = 0       #number of pixels counted
    roast_level = 0 #overall roast level

    #ensuring that there are some interior pixels
    if(len(pixs[0]) > 0):

        #working through all interior pixels
        for i in range(len(pixs[0])):
        
            #summing up the grayscale value for level of "darkening
            pix_dark += img[pixs[0][i],pixs[1][i]]
            count +=1

        #final calculation of darkness
        roast_level = pix_dark/float(count)
    
    return roast_level


if __name__ == "__main__":

    #dasic video capture object
    videoCap = cv2.VideoCapture(0)

    #checking successful video capture creation
    if(not videoCap.isOpened()):
        print ("ERROR CANT FIND PI CAMERA")
        quit()
    else:
        print("camera found")


    #reading in an initial frame
    b, image = videoCap.read()

    #continuously reading in camera data
    while True:

        #reading in a frame
        b, image = videoCap.read()

        #adjusting for more processing
        im_resize = imutils.resize(image, width=300)
        ratio = image.shape[0]/float(im_resize.shape[0])
    
        #image processing steps
        gray = cv2.cvtColor(im_resize, cv2.COLOR_BGR2GRAY)  #grayscale
        blurred = cv2.GaussianBlur(gray, (5,5), 0)          #slight blurring
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]  #thresholding for shape

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
                c_new = (c.astype("float")*ratio).astype('int')
                cv2.drawContours(image, [c_new], -1, RED,-1)
                cv2.putText(image, status, (c_x,c_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
                #displaying the associated toastedness
                roastLevel = RoastLevel(c,gray)
                cv2.putText(image, str(roastLevel), (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)


        cv2.imshow("Gray", gray)
        cv2.imshow("Image", image)
        cv2.waitKey(1)
