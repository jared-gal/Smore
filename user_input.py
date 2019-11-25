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
font = pygame.font.Font(None, 50)

#setting up pygame
screen = pygame.display.set_mode(size)
screen.fill(BLACK)

#importing images
l_0 = pygame.image.load("l_0.pyng")
l_1 = pygame.image.load("l_1.png")
l_2 = pygame.image.load("l_2.png")
l_3 = pygame.image.load("l_3.png")
l_4 = pygame.image.load("l_4.png")
l_5 = pygame.image.load("l_5.png")
l_6 = pygame.image.load("l_6.png")
l_7 = pygame.image.load("l_7.png")
l_8 = pygame.image.load("l_8.png")
l_9 = pygame.image.load("l_9.png")
l_10 = pygame.image.load("l_10.png")
default = pygame.image.load("smore.png")

#interrupts for the two buttons
#increase toast level
def gpio22(channel):
    global Toast_Level
    Toast_Level = Toast_Level + 1
    if(Toast_Level > 10):
        Toast_Level = 10
    print("More Toastedness")

#decrease Toast Level
def gpio23(channel):
    global Toast_Level
    Toast_Level = Toast_Level - 1
    if(Toast_Level <0):
        Toast_Level = 0
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
        sys.exit()

#a function that determines what image to display on the TFT
def pick_im():
    switcher = {
        0:l_0,
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

        #blitting desired image to display
        sreen.blit(image_toast, im_rect)

        if (Proceed is False):
            my_buttons = {'Select':(300,225), 'Darker':(300,155), 'Lighter':(300,85), 'Quit':(300,15)}
            for my_text, text_pos in my_buttons.items():
                text_surface = my_font.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)

        else:
            my_buttons = {'Is this the Correct Amount of Toastedness':(160,120), 'Confirm':(300,225), 'Cancel':(300,15)}
            for my_text, text_pos in my_buttons.items():
                text_surface = my_font.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)

        #flipping the display
        pygame.display.flip()


