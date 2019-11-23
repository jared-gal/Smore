#!/usr/bin/python

#this is a script to test the ability to select a particular 
#contour to analyze and disregard all others

import cv2
import numpy as np
import imutils
import RPi.GPIO as GPIO

#setting up relevant GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)


#glodal Variables
Proceed = False
Next_Cont = False
RED = (255,0,0)
WHITE = (255,255,255)

#interrupts for the two buttons
def gpio17(channel):
    global Proceed
    Proceed = True
    print("Proceeding")


def gpio27(channel):
    global Next_Cont
    Next_Cont = True
    print("Next Contour")




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
    
    #returning the contour status as potential mallow or not
    return status


if __name__ == "__main__":

    #mallow contour
    mc = []
    
    #setting up callbacks
    GPIO.add_event_detect(17, GPIO.FALLING, callback = gpio17, bouncetime = 300)
    GPIO.add_event_detect(27, GPIO.FALLING, callback = gpio27, bouncetime = 300)

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
        
        count = 0
        #find shapes based on contours
        for c in conts:
            Proceed = False
            Next_Cont = False
            #finding the center of the contour using moments
            M=cv2.moments(c)
            c_x = 75
            c_y = 75
            status = ShapeDetector(c)
            if(status == "MARSHMALLOW"):
                #convert the contour to a drawable shape
                c_new = (c.astype("float")*ratio).astype('int')
                #draw name of shape on contour at (x,y) coords
                cv2.drawContours(image, [c_new], -1, RED,-1)
                cv2.putText(image, status, (c_x,c_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
                #displaying the associated toastedness
                text = "Contour #" + str(count)
                
                cv2.putText(image, text, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
                count +=1
                cv2.imshow("Gray", gray)
                cv2.imshow("Image", image)
                cv2.waitKey(1)


                while (Next_Cont is False) and (Proceed is False):
                    if(Proceed is True):
                        mc = c_new
                        break

        
        cv2.imshow("Gray", gray)
        cv2.imshow("Image", image)
        cv2.waitKey(1)

    print("Contour Confirmed")
    cv2.imshow("Gray", gray)
    cv2.imshow("Image", image)
    cv2.waitKey(1)

