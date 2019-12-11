#!/usr/bin/python

#this is a script to test the ability to select a particular 
#contour to analyze and disregard all others

import cv2
import numpy as np
import imutils
import RPi.GPIO as GPIO
import time
import os


#glodal Variables
Proceed = False
Next_Cont = False
RED = (255,0,0)
WHITE = (255,255,255)
end = False


#interrupts for the two buttons
#17 selects a contour
def gpio17_pc(channel):
    global end
    end = True

#27 says to cycle to another contour
def gpio27_pc(channel):
    global Next_Cont
    Next_Cont = True

#this function detects the presence of contours that could be marshmallows
def ShapeDetector(c):
    
    #base case of no mallow
    status = "Invalid"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, .01*peri, True)

    #detecting if a contour large enough to be the marshmallow is found
    if peri > 100:
        status = "Valid"

    #returning the contour status as potential mallow or not
    return status


def main():

    #defining global variables
    global Proceed
    global Next_Cont
    global end

    #setting up relevant GPIO pins for interrupts
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    #aligning the servo properly for analysis
    GPIO.setup(5, GPIO.OUT)
    pin = GPIO.PWM(5,50)
    pin.start(2.5)
    time.sleep(2)
    pin.start(0)

    
    #to hold the final mallow contour
    mc = []
    
    #setting up callbacks
    GPIO.add_event_detect(17, GPIO.FALLING, callback = gpio17_pc, bouncetime = 300)
    GPIO.add_event_detect(27, GPIO.FALLING, callback = gpio27_pc, bouncetime = 300)

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
    end = False

    #start time to allow for a short feed of setup
    start_time = time.time()

    #continuously reading camera data until the desired contour is identified
    while not end:

        #reading in a frame
        b, image = videoCap.read()

        #adjusting for more processing
        image = imutils.resize(image, width=320, height = 240)
        
        #selecting only a particular area of the image based on limitations of mallow 
        image = image[50:220,80:220] 
        image = imutils.resize(image,width=320, height =240)
        
        #image processing steps
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #grayscale
        blurred = cv2.GaussianBlur(gray, (5,5), 0)          #slight blurring
        thresh = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY)[1]  #thresholding for shape

        #contour finding
        conts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        conts = imutils.grab_contours(conts)
        
        #find shapes based on contours
        for i in range(len(conts)):
            Proceed = False
            Next_Cont = False
            
            #determining the validity of a given contour
            status = ShapeDetector(conts[i])
            #image copy so we can see one contour at a time
            n_im = image.copy()
            if status == "Valid":
                
                #draw contour on image
                cv2.drawContours(n_im, conts, i, RED,2)

                #show the image with one contour
                cv2.imshow("Image", n_im)
                cv2.waitKey(1)

                if (time.time() - start_time)>3:
                    while (Next_Cont is False):
                        if(end is True):
                            c = conts[i]
                            
                            print("Cont Conf #")
                            print(i)
                            GPIO.cleanup()
                            return c,i
                            break
                        else:
                           a=1 


    print("Contour Error")
    GPIO.cleanup()
    return [],-1

