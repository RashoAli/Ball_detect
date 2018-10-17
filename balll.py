# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import argparse
import cv2
import imutils
import time

from Ball_funk import Ball_objekt

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=0).start()

# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)
greenLower = (80, 40, 6)  # anfang werte fur die fabe
greenUpper = (120, 255, 255)
# Define the codec and create VideoWriter object
# deklerait ball_Objekt
Ball_1 = Ball_objekt()
is_ball_hist_created = False
# keep looping
while True:
    frame = vs.read()
    if not is_ball_hist_created:
        farme = Ball_1.draw_rect(frame, is_ball_hist_created)
        hsv_data = Ball_1.hand_histogram(frame)
        pressed_key = cv2.waitKey(1)
        if pressed_key & 0xFF == ord('z'):
            greenLower = (hsv_data[0, 0], hsv_data[1, 0], hsv_data[2, 0])
            greenUpper = (hsv_data[0, 1], hsv_data[1, 1], hsv_data[2, 1])
            is_ball_hist_created = True
    ''' re_calibration fals gebraucht wird '''
    re_calibration_key = cv2.waitKey(1)
    if re_calibration_key & 0xFF == ord('r'):
        is_ball_hist_created = False

    # grab the current frame
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None

    # only proceed if at least one contour was for
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size

        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    # update the points queue
    pts.appendleft(center)
    # update HSV range

    if is_ball_hist_created:
        Ball_1.draw_moving_rect(frame, x, y, radius)
        Flag = Ball_1.chek_x_y(frame)
        if not Flag:
            frame = Ball_1.draw_rect(frame, is_ball_hist_created)
            hsv_data = Ball_1.hand_histogram(frame)
            greenLower = (hsv_data[0, 0], hsv_data[1, 0], hsv_data[2, 0])
            greenUpper = (hsv_data[0, 1], hsv_data[1, 1], hsv_data[2, 1])

    # loop over the set of tracked points
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    # print(radius)

    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera
else:
    vs.release()
# close all windows
cv2.destroyAllWindows()
