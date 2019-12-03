#!/usr/bin/python

#this script is to run the sub programs of SMORE project
import user_input as usr
import pick_contour as pc
import RPi.GPIO as GPIO

if __name__ == "__main__":
    #getting the desired contour for the mallow
    C = pc.main()
    print("Returned Contour is:")
    print (C)

    #getting the user selected level of toastedness
    TL = usr.main()
    print("Returned Value is:")
    print(TL)


