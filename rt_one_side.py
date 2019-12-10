#!/usr/bin/python

#this is a script to read in camera data of a detected marshmallow, and read it's toastedness
#toastedness will be done via averaging pixel data of detected marshmallow shape
#script also rotates the toasting stepper and 
#TODO
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

#contour that is the mallow
Mallow_Cont = []
#desired toastedness of the mallow
Toast_Level = 0

#average array
Avg_Toast = []
start_toast = 255
Index = 0
init_rt = True

def gpio17(channel):
    print("forced retrieval")
    sys.exit()


#this function takes in a grayscale image and a given contour to find
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

        #if just starting then the first reading is of the untoasted side
        #so we want a base darkness value
    
    return roast_level


def main(TL,C):

    #global
    global Mallow_Cont
    global Toast_level
    global start_toast
    global init_rt

    init_rt = True
    
    Mallow_Cont = C
    Toast_Level = TL
    #setting up GPIO to turn mallow
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)

    GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    #ccw at .1 is  46.486 w dc of 7.063
    #cw is 46.554 with 6.89
    #basic video capture object
    videoCap = cv2.VideoCapture(0)

    #checking successful video capture creation
    if(not videoCap.isOpened()):
        print ("ERROR CANT FIND PI CAMERA")
        quit()
    else:
        print("camera found")

    pin = GPIO.PWM(5,50)
    pin.start(2.5)
    print("Turn up")
    #reading in an initial frame
    b, image = videoCap.read()

    image = imutils.resize(image, width = 320, height =240)
    image = image[70:220, 70:220]
    #image processing steps
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #grayscale

    #init roast level
    count = 0
    roastLevel = 0
    for i in range(0,5):
        count += 1
        roastLevel += RoastLevel(gray)

    start_toast = roastLevel/float(count)
    roastLevel = start_toast
    print("turn down")
    pin.ChangeDutyCycle(7.5)
    time.sleep(2)
    pin.ChangeDutyCycle(0)

    #converting toast level to darkness value
    cookLevel = 10 +  Toast_Level*2
    print("Cook Level is")
    print (cookLevel)
    time_start = time.time() 
    update = True

    while start_toast-roastLevel < cookLevel :
        #every 20 seconds we recheck toastedness
            if(time.time()-time_start) > 20 :
                #rotating mallow back into view
                pin.ChangeDutyCycle(2.5)
                time.sleep(1.7)
                pin.ChangeDutyCycle(0)

                #updating roast level based on 5 sample average
                roastLevel = 0
                count = 0
                for i in range(0,5):
                    #reading in a frame
                    b, image = videoCap.read()

                    #adjusting for more processing
                    image = imutils.resize(image, width = 320, height =240)
                    image = image[70:220, 70:200]
                    #image processing steps
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #grayscale
                    #calculating toastedness
                    count += 1
                    roastLevel += RoastLevel(gray)

                roastLevel = roastLevel/float(count)

                #rotating mallow back to heat
                pin.ChangeDutyCycle(7.5)
                time.sleep(1.7)
                pin.ChangeDutyCycle(0)
                time_start = time.time()

            #reading in a frame when not processing
            b, image = videoCap.read()

            #adjusting for more processing
            image = imutils.resize(image, width = 320, height =240)
            image = image[70:220, 70:200]

            #displaying the toastedness level of the desired contour
            #location of printing
            c_x = 0 
            c_y = 75
        
            #draw contour and output roast val 
            cv2.drawContours(image, [Mallow_Cont], -1, RED,1)
            cv2.putText(image, "Last Roast Value", (c_x,c_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
            cv2.putText(image, str(roastLevel), (50,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
            

            image = imutils.resize(image, width = 320, height = 240)
            cv2.imshow("Image", image)
            cv2.waitKey(1)
    print("final roast level is:")
    print (roastLevel)
    pin.ChangeDutyCycle(7)
    time.sleep(.5)
    pin.ChangeDutyCycle(0)
    GPIO.cleanup()
