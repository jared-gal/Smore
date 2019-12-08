#!/usr/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
pin = GPIO.PWM(4,1)
GPIO.setup(19,GPIO.OUT)

pin.start(50)
pin.ChangeFrequency(100)
GPIO.output(19,1)

usr_in = 0
while usr_in is not 1:
    time.sleep(.1)
    usr_in = raw_input("1 enter to quit")
    usr_in = int(usr_in)

GPIO.cleanup()
