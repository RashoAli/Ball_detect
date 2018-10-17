# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

from Ball_funk import Ball_Objekt

'''' beim angfang kay : c = calibrating
                        r = re_calibrating
                        q = end             '''


vs = VideoStream(src=0).start()

# allow the camera or qqvideo file to warm up
time.sleep(2.0)
greenLower = (40, 40, 6)  # anfang werte fur die fabe
greenUpper = (120, 255, 255)
# Define the codec and create VideoWriter object
# deklerait ball_Objekt
Ball_1 = Ball_Objekt()
is_ball_hist_created = False
# keep looping
while True:
    frame = vs.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    #frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    hsv[hsv[:, :, 0] < 50] = 0
    hsv[hsv[:, :, 0] > 180] = 0

    # check to calibrate the color borders
    if not is_ball_hist_created:
        farme = Ball_1.draw_rect(frame, is_ball_hist_created)
        hsv_data = Ball_1.hand_histogram(frame)
        pressed_key = cv2.waitKey(1)
        if pressed_key & 0xFF == ord('c'):
            greenLower = (hsv_data[0, 0], hsv_data[1, 0], hsv_data[2, 0])
            greenUpper = (hsv_data[0, 1], hsv_data[1, 1], hsv_data[2, 1])
            is_ball_hist_created = True

    ''' re_calibration fals gebraucht wird '''
    re_calibration_key = cv2.waitKey(1)
    if re_calibration_key & 0xFF == ord('r'):
        is_ball_hist_created = False


    # update HSV range
    if is_ball_hist_created:
        Ball_1.draw_moving_rect(frame)
        Flag = Ball_1.chek_x_y(frame)
        if not Flag:
            frame = Ball_1.draw_rect(frame, is_ball_hist_created)
            hsv_data = Ball_1.hand_histogram(frame)
            greenLower = (hsv_data[0, 0], hsv_data[1, 0], hsv_data[2, 0])
            greenUpper = (hsv_data[0, 1], hsv_data[1, 1], hsv_data[2, 1])


    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    center,radius = Ball_1.find_contur(mask)
    if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(center[0]), int(center[1])), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # loop over the set of tracked points
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    # print(radius)

    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break


# otherwise, release the camera
else:
    vs.release()
# close all windows
cv2.destroyAllWindows()
