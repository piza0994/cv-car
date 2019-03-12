import time
 
import cv2
import numpy as np
from imutils.video import VideoStream
import imutils
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()
 
# Are we using the Pi Camera?
usingPiCamera = False
# Set initial frame size.
frameSize = (360, 360)
 
# Initialize mutithreading the video stream.
vs = VideoStream(src=0, usePiCamera=usingPiCamera, resolution=frameSize,
        framerate=3).start()
# Allow the camera to warm up.
time.sleep(2.0)
 
timeCheck = time.time()
while True:
    # Get the next frame.
    frame = vs.read()
    
    # If using a webcam instead of the Pi Camera,
    # we take the extra step to change frame size.
    if not usingPiCamera:
        frame = imutils.resize(frame, width=frameSize[0])
     
    #frame = cv2.GaussianBlur(frame, (7, 7), 1.41)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    #define range of blue color in HSV
    lower_blue = np.array([101,50,50])
    upper_blue = np.array([130,255,255])
    mask = cv2.inRange(hsv,lower_blue,upper_blue)
    
    #bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame,frame,mask = mask)
    
    ret,thresh = cv2.threshold(mask,127,255,1)

    _,contours,h = cv2.findContours(thresh,1,2)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        
        if len(approx)== 7:
            approx_length = approx[1][0][0] - approx[3][0][0];
            if approx_length >= 30:
                print ("approx_length: ", approx_length)
                print("derecha")
                b = bytes('1', 'utf-8')
                ser.write(b)
            elif approx_length < -30:
                print ("approx_length: ", approx_length)
                print("izquierda")
                b = bytes('2', 'utf-8')
                ser.write(b)
            cv2.drawContours(mask,[cnt],0,255,-1)
            

    # Show video stream
    cv2.imshow('original', frame)
    cv2.imshow('gray', gray)
    cv2.imshow('mask', mask)
    key = cv2.waitKey(50) & 0xFF
 
    # if the `q` key was pressed, break from the loop.
    if key == ord("q"):
        break
    #time.sleep(0.5)
    #print(1/(time.time() - timeCheck))
    #timeCheck = time.time()
 
# Cleanup before exit.
cv2.destroyAllWindows()
vs.stop()

