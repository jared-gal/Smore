#!/usr/bin/python
import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
servo_pin = GPIO.PWM(6, 46.598)
servo_pin.start(6.803)
usr_in = "fish"

while usr_in != "done":
    usr_in = raw_input("done to end")
    time.sleep(.01)
    
GPIO.cleanup()
