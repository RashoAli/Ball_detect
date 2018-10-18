# import the necessary packages
from imutils.video import VideoStream
import cv2
import time
import matplotlib.pyplot as plt
from Ball_funk import mask_producer,ObjektBall
import numpy as np

'''' am Angfang kay : c = calibrating
                        r = re_calibrating
                        q = end             '''

slider_var = False

if slider_var:
    def nothing(x):
        pass


    # Create a black image, a window
    temp_img = np.zeros((300, 512, 3), np.uint8)
    cv2.namedWindow('image')

    # create trackbars for color change
    cv2.createTrackbar('H1', 'image', 0, 255, nothing)
    cv2.createTrackbar('h1', 'image', 0, 255, nothing)
    switch = '0 : OFF \n1 : ON'
    cv2.createTrackbar(switch, 'image', 0, 1, nothing)

vs = VideoStream(src=0).start()

# allow the camera or qqvideo file to warm up
time.sleep(2.0)
greenLower = (40, 40, 6)  # anfang werte fur die fabe
greenUpper = (120, 255, 255)
# Define the codec and create VideoWriter object
# deklerait ball_Objekt
is_ball_hist_created = False
# keep looping
while True:
    if slider_var:
        cv2.imshow('image', temp_img)
        H1 = cv2.getTrackbarPos('H1', 'image')
        h1 = cv2.getTrackbarPos('h1', 'image')

    frame = vs.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    median = cv2.medianBlur(frame, 5)
    mask_HSV = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)

    Blau_mask, Blau_c = mask_producer(frame, mask_HSV, 'Blau')
    Grun_mask, Grun_c = mask_producer(frame, mask_HSV, 'Grun')

    cv2.imshow('Blau_mask', Blau_mask)
    cv2.imshow('Grun_mask', Grun_mask)
    cv2.imshow("Frame", frame)
    # print(radius)
    #plt.imshow(mask_HSV)
    #plt.show()
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break


# otherwise, release the camera
else:
    vs.release()
# close all windows
cv2.destroyAllWindows()
