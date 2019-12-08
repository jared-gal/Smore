#!/usr/bin/python

#this script is to run the sub programs of SMORE project
import user_input as usr
import pick_contour as pc
import read_toast_update as rt
import retrieve as re

if __name__ == "__main__":
   # getting the desired contour for the mallow
    #C,I = pc.main()

    #getting the user selected level of toastedness
    #TL = usr.main()

    #reading the toastiness of the contour until desired level is reached
    #TODO
    #make read toast update have rolling average of ~2 sec
    #rt.main(TL,C)   

    #script that retrieves the mallow and makes the smore
    #TODO
    re.main()
