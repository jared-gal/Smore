#!/usr/bin/python

#this script is to run the sub programs of SMORE project
import user_input as usr
import pick_contour as pc
import rt_one_side as rt
import retrieve as re
import time
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13,0)

#os.putenv('SDL_VIDEODRIVER','fbcon')
#os.putenv('SDL_FBDEV','/dev/fb1')

if __name__ == "__main__":
    
    GPIO.cleanup()

   # getting the desired contour for the mallow
    C,I = pc.main()

    #slight delay between programs
    time.sleep(1)

    #getting the user selected level of toastedness
    TL = usr.main()

    #reading the toastiness of the contour until desired level is reached
    rt.main(TL,C)   
    
    print("waiting for 5 seconds to cool off")
    time.sleep(5)

    #script that retrieves the mallow and makes the smore
    re.main()
