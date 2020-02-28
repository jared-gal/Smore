#!/usr/bin/python

#this is a script to read in camera data of a detected marshmallow, and read it's toastedness
#toastedness will be done via averaging pixel data of detected marshmallow shape
#script also 
#controls heating element activation

import sys
import cv2
import numpy as np
import imutils
import RPi.GPIO as GPIO
import time 

#basic color definitions
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

#contour that is the mallow
Mallow_Cont = []
enter_retrieval = False

#desired toastedness of the mallow
Toast_Level = 0

#starting toast level
start_toast = 255

#forced exit from program
def gpio17(channel):
    print("forced retrieval")
    GPIO.output(13,0)
    global enter_retrieval 
    enter_retrieval = True


#this function takes in a grayscale image and uses the mallow contour to find
#the darkening of the specific region bound by the contour
def RoastLevel(img):

    global Mallow_Cont
    c = Mallow_Cont
    
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

#takes the toastedness level and mallow contour from prior scripts,
#this function will monitor the toastedness of a side of the mallow 
def main(TL,C):

    #global variables necessary
    global Mallow_Cont
    global Toast_level
    global enter_retrieval
    
    Mallow_Cont = C
    Toast_Level = TL
    
    #setting up GPIO to turn mallow
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)

    #interrupt to force mallow retrieval if necessary
    GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    #setting up callbacks
    GPIO.add_event_detect(17, GPIO.FALLING, callback = gpio17, bouncetime = 300)
    
    #pin used to turn on heating element
    GPIO.setup(13, GPIO.OUT)
    GPIO.output(13,0)

    #basic video capture object
    videoCap = cv2.VideoCapture(0)

    #checking successful video capture creation
    if(not videoCap.isOpened()):
        print ("ERROR CANT FIND PI CAMERA")
        quit()
    else:
        print("camera found")

    #turning on the heating element and aligning the mallow
    GPIO.output(13,1)
    time.sleep(4.5)
    
    #aligning the mallow
    pin = GPIO.PWM(5,50)
    pin.start(2.5)
    time.sleep(1)
    pin.start(0)
    
    
    #init roast level
    count = 0
    roastLevel = 0
    start_toast = 0

    pin.ChangeDutyCycle(7.5)
    time.sleep(2)
    pin.ChangeDutyCycle(0)

    #converting toast level to darkness value
    cookLevel = 1 +  Toast_Level*1.5
    
    
    time_start = time.time()
    time_begin = time.time()
    update = True
    init = True
    init_2 = True
    
    while (start_toast-roastLevel < cookLevel) and (enter_retrieval is False) and (time.time() - time_begin < 300):
        #every 10 seconds we recheck toastedness
            if(time.time()-time_start) > 10 or init:
                #rotating mallow back into view
                pin.ChangeDutyCycle(2.5)
                time.sleep(1.7)
                pin.ChangeDutyCycle(0)

                #updating roast level based on 5 sample average
                roastLevel = 0
                count = 0
                for i in range(0,5):
                    #small delay
                    time.sleep(.1)

                    #reading in a frame
                    b, image = videoCap.read()

                    #adjusting for more processing
                    image = imutils.resize(image, width = 320, height =240)
                    image = image[40:220, 70:220]
                    image = imutils.resize(image, width =320, height=240)
                    
                    #image processing steps
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #grayscale
                    
                    #calculating toastedness
                    count += 1
                    roastLevel += RoastLevel(gray)
                
                #finding final average roastLevel
                roastLevel = roastLevel/float(count)
                if init is False and init_2 is True:
                    start_toast = roastLevel -1
                    init_2 = False

                    #determining what the target darkness level is
                    print("Starting Roast Level is:")
                    print ((start_toast))
                    print("Cook Level is:")
                    print ((cookLevel))
                    print("Target Roast Level is:")
                    print ((start_toast - cookLevel))

                init = False
                #rotating mallow back to heat
                pin.ChangeDutyCycle(7.5)
                time.sleep(1.7)
                pin.ChangeDutyCycle(0)
                time_start = time.time()

            #reading in a frame when not checking the toastedness
            b, image = videoCap.read()

            #adjusting for more processing
            image = imutils.resize(image, width = 320, height =240)
            image = image[40:220, 70:220]
            image = imutils.resize(image, width =320, height=240)
            
            #displaying the toastedness level of the desired contour
            #location of printing
            c_x = 20
            c_y = 75
        
            #draw contour (not enabled now) and output roast val 
            #cv2.drawContours(image, [Mallow_Cont], -1, RED,1)
            cv2.putText(image, "Last Roast Value", (c_x,c_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, BLACK, 2)
            cv2.putText(image, str(round(roastLevel)), (20,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, BLACK, 2)
            
            #displaying image
            cv2.imshow("Image", image)
            cv2.waitKey(1)
       
    #turning off heating element
    GPIO.output(13,0)
    
    #outputting final roast level
    print("final roast level is:")
    print (roastLevel)
    
    #aligning skewers for extraction
    pin.ChangeDutyCycle(7)
    time.sleep(.5)
    pin.ChangeDutyCycle(0)
    GPIO.cleanup()
