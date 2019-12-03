#!/usr/bin/python

#this script is to run the sub programs of SMORE project
import user_input as usr
import pick_contour as pc
import read_toastiness as rt

if __name__ == "__main__":
    #getting the desired contour for the mallow
    C = pc.main()
    print("Returned Contour is:")
    print (C)

    #getting the user selected level of toastedness
    TL = usr.main()
    print("Returned Value is:")
    print(TL)

    #reading the toastiness of the contour until desired level is reached
    #TODO
    #make read toastwork for a main function with args
    #make read toast be responsible for rotating servo with mallow
    #make RT handle turning on and off heating element
    rt.main(TL,C)   


    #TODO
    #need to implement a script that will grab the mallow
