# import the necessary packages
from imutils.video import VideoStream
import cv2
import time
import matplotlib.pyplot as plt
from Ball_funk import Ball_Objekt, mask_producer
import numpy as np

'''' beim angfang kay : c = calibrating
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
Ball_1 = Ball_Objekt()
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

    # resize the frame, blur it, and convert it to the HSV
    # color space
    # frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # plt.imshow(hsv)
    # plt.show()
    # mask_LAB = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
    mask_HSV = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    Blau_mask, Blau_c = mask_producer(frame, mask_HSV, 'Blau')
    Grun_mask, Grun_c = mask_producer(frame, mask_HSV, 'Grun')

    cv2.imshow('Blau_mask', Blau_mask)
    cv2.imshow('Grun_mask', Grun_mask)

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
    center, radius = Ball_1.find_contur(mask)


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
