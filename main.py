import cv2 as cv
import numpy as np
import os
#from matplotlib import pyplot as plt
#read the reference row image
row = cv.imread("row.jpg")
#Start videocapture from web cam(0)
cap = cv.VideoCapture(0)
MatchesCounter =0
while(True):
    #Capture frame-by-frame
    ret,frame = cap.read()
    #turn the image to gray scale
    img_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    kernel = np.ones((5,5),np.float32)/25

    #dst = cv.filter2D(img_gray,-1,kernel)
    #dst_bgr = cv.filter2D(frame,-1,kernel)
    #canny = cv.Canny(dst,20,150)
    canny = cv.Canny(img_gray,50,150)
    #Obtain values of canny
    height, width, channels= frame.shape
    #draw only contours
    
    contours = np.zeros((height , width, channels), dtype = "uint8")
    ret, thresh = cv.threshold(canny, 50, 150, 0)
    c, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #c = imutils.grab_contours(c)
    c = sorted(c,key =cv.contourArea, reverse=True)
    cv.imshow('canny',canny)
    cv.imshow('frame',frame)
    siz = len(c)
    i =0
#     while(i<siz):
#             contours = np.zeros((height , width, channels), dtype = "uint8")
#             cv.drawContours(contours, c, i, (0,255,0), 1)
#             #First check it matches 
#             #cv.phaseCorrelate(row,contours)

#             #display the resulting frame
#             if cv.waitKey(1) & 0xFF == ord('a'):        
#                 cv.imshow('contours',contours)
#                 i=i+1
#             elif cv.waitKey(1) & 0xFF == ord('z'):
#                 break;


    if cv.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv.destroyAllWindows()

