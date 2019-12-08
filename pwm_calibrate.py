#!/usr/bin/python
import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
servo_pin = GPIO.PWM(5, 46.51)
servo_pin.start(6.977)
usr_in = "fish"

while usr_in != "done":
    usr_in = raw_input("done to end")
    time.sleep(.01)
    
GPIO.cleanup()
