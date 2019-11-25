#!/usr/bin/python

#this is a script to take basic user input

import numpy as np
import RPi.GPIO as GPIO
import pygame
import os
import sys
pygame.init()

#TFT Stuff
#TODO


#setting up relevant GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)


#global variables
Toast_Level = 0
Confirmed = False
Proceed = False
size = width,height = 320,240
WHITE = 255,255,255
BLACK = 0,0,0
my_font = pygame.font.Font(None, 25)

#setting up pygame
screen = pygame.display.set_mode(size)
screen.fill(BLACK)

#importing images
l_1 = pygame.image.load("l_1.jpg")
l_2 = pygame.image.load("l_2.jpg")
l_3 = pygame.image.load("l_3.jpg")
l_4 = pygame.image.load("l_4.jpg")
l_5 = pygame.image.load("l_5.jpg")
l_6 = pygame.image.load("l_6.jpg")
l_7 = pygame.image.load("l_7.jpg")
l_8 = pygame.image.load("l_8.jpg")
l_9 = pygame.image.load("l_9.jpg")
l_10 = pygame.image.load("l_10.jpg")
default = pygame.image.load("default.jpg")

#interrupts for the two buttons
#increase toast level
def gpio22(channel):
    if Proceed is False:
        global Toast_Level
        Toast_Level = Toast_Level + 1
        if(Toast_Level > 10):
            Toast_Level = 10
        print("More Toastedness")

#decrease Toast Level
def gpio23(channel):
    if Proceed is False:
        global Toast_Level
        Toast_Level = Toast_Level - 1
        if(Toast_Level <1):
            Toast_Level = 1
        print("Less Toastedness")
    
#confirm toast level
def gpio17(channel):
    global Proceed
    global Confirmed
    if(Proceed is True):
        Confirmed = True
        print("Confirmed")

    else:
        Proceed = True
        print("Proceeding")

#cancel toast level
def gpio27(channel):
    global Proceed
    if Proceed is True:
        Proceed = False
    else:
        GPIO.cleanup()
        sys.exit()

#a function that determines what image to display on the TFT
def pick_im():
    switcher = {
        1:l_1,
        2:l_2,
        3:l_3,
        4:l_4,
        5:l_5,
        6:l_6,
        7:l_7,
        8:l_8,
        9:l_9,
        10:l_10,
    }
    return switcher.get(Toast_Level, default)

if __name__ == "__main__":

    #setting up callbacks
    GPIO.add_event_detect(17, GPIO.FALLING, callback = gpio17, bouncetime = 300)
    GPIO.add_event_detect(27, GPIO.FALLING, callback = gpio27, bouncetime = 300)
    GPIO.add_event_detect(22, GPIO.FALLING, callback = gpio22, bouncetime = 300)
    GPIO.add_event_detect(23, GPIO.FALLING, callback = gpio23, bouncetime = 300)
    
    
    #continuously updating TFT
    while not Confirmed:

        #reading what image to display
        image_toast = pick_im()
        im_rect = image_toast.get_rect()
        screen.fill(BLACK)
        #blitting desired image to display
        screen.blit(image_toast, im_rect)

        if (Proceed is False):
            my_buttons = {'Select':(290,15), 'Darker':(290,155), 'Lighter':(290,85), 'Quit':(300,225)}
            for my_text, text_pos in my_buttons.items():
                text_surface = my_font.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)

        else:
            my_buttons = {'Correct Amount of Toastedness?':(160,120), 'Confirm':(290,15), 'Cancel':(290,225)}
            for my_text, text_pos in my_buttons.items():
                text_surface = my_font.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)

        #flipping the display
        pygame.display.flip()



