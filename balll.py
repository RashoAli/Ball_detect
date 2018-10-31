# import the necessary packages
from imutils.video import VideoStream
import cv2
import time
import matplotlib.pyplot as plt
from Ball_funk import mask_producer, coordinat_zu_ordnen
import numpy as np

'''' am Angfang kay : c = calibrating
                        r = re_calibrating
                        q = end             '''

slider_var = False  # if True you can change H1,h1 variables dynamically

if slider_var:
    def nothing():
        pass

    # Create a black image, a window
    temp_img = np.zeros((300, 512, 3), np.uint8)
    cv2.namedWindow('image')

    # create trackbars for color change
    cv2.createTrackbar('H1', 'image', 30, 255, nothing)
    cv2.createTrackbar('h1', 'image', 20, 255, nothing)
    switch = '0 : OFF \n1 : ON'
    cv2.createTrackbar(switch, 'image', 0, 1, nothing)

vs = VideoStream(src=0).start()

# allow the camera to warm up
time.sleep(2.0)

detected_Balls = []
frame_number = 0

# keep looping
while True:
    frame_number = frame_number + 1

    """ bei assigning H1 and h1 to a variable it can be dynamically changed """
    if slider_var:
        cv2.imshow('image', temp_img)
        H1 = cv2.getTrackbarPos('H1', 'image')
        h1 = cv2.getTrackbarPos('h1', 'image')

    frame = vs.read()
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    """erzeug HSV,Gray masken um weitter die bälle zu finden"""
    median = cv2.medianBlur(frame, 5)
    mask_HSV = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)
    mask_gray = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)

    """finde wo das Ball(mittelpunkt ,Radius)"""
    Blau_mask, Blau_c = mask_producer(frame, mask_HSV, 'Blau', frame_number)  # output -> mask,(x,y,r,distanz)
    # Grun_mask, Grun_c = mask_producer(frame, mask_HSV, 'Grun',frame_number)

    """speicher die gefundene bälle in eine liste detected_Balls"""
    if Blau_c != []:  # wenn es Blaue ball gibt
        detected_Balls = coordinat_zu_ordnen('Blau', Blau_c, detected_Balls)
    # if Grun_c != []: # wenn es Grune ball gibt
    # detected_Balls = coordinat_zu_ordnen('Grun', Grun_c, detected_Balls)

    """show the frame and other stuff"""
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", Blau_mask)

    # if the 'q' key is pressed, stop the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close all windows
vs.stop()
cv2.destroyAllWindows()
