#!/usr/bin/python

#this is a script to test the ability to select a particular 
#contour to analyze and disregard all others

import cv2
import numpy as np
import imutils
import RPi.GPIO as GPIO
import time


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
    print("Proceeding")

#27 says to cycle to another contour
def gpio27_pc(channel):
    global Next_Cont
    Next_Cont = True
    print("Next Contour")




#this function detects the presence of a marshmallow
def ShapeDetector(c):
    #base case of no mallow
    status = "Invalid"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, .01*peri, True)

    #detecting if a rectangular shape is found (cross section of marshmallow
    if peri > 200:
        status = "Valid"

    #returning the contour status as potential mallow or not
    return status


def main():
    


    #defining global variables
    global Proceed
    global Next_Cont
    global end

    #setting up relevant GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)



    
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
    #continuously reading in camera data

    #start time
    start_time = time.time()

    while not end:

        #reading in a frame
        b, image = videoCap.read()

        #adjusting for more processing
        #im_resize = imutils.resize(image, width=300)
        #ratio = image.shape[0]/float(im_resize.shape[0])
        image = imutils.resize(image, width=320, height = 240)
        image = image[70:220, 70:220] 
        #image processing steps
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #grayscale
        blurred = cv2.GaussianBlur(gray, (5,5), 0)          #slight blurring
        thresh = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY)[1]  #thresholding for shape

        #contour finding and rectangle identification
        conts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        conts = imutils.grab_contours(conts)
        
        count = 0
        #find shapes based on contours
        for i in range(len(conts)):
            Proceed = False
            Next_Cont = False
            
            c_x = 75
            c_y = 75
            status = ShapeDetector(conts[i])
            n_im = image.copy()
            if status == "Valid":
                
		#convert the contour to a drawable shape
                #c_new = (c.astype("float")*ratio).astype('int')
                #draw name of shape on contour at (x,y) coords
                cv2.drawContours(n_im, conts, i, RED,-1)
                cv2.putText(n_im, status, (c_x,c_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
                #displaying the associated toastedness
                text = "Contour #" + str(count)
                
                cv2.putText(n_im, text, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
                cv2.imshow("Gray", gray)
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

