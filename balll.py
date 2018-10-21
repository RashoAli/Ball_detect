# import the necessary packages
from imutils.video import VideoStream
import cv2
import time
import matplotlib.pyplot as plt
from Ball_funk import mask_producer, coordinat_zu_ordnen
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

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
    cv2.createTrackbar('H1', 'image', 30, 255, nothing)
    cv2.createTrackbar('h1', 'image', 20, 255, nothing)
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
detected_Balls = []
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
    """erzeug HSV,Gray masken um weitter die bälle zu finden"""
    median = cv2.medianBlur(frame, 5)
    mask_HSV = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)
    mask_gray = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)

    """finde wo das Ball(mittelpunkt ,Radius)"""
    Blau_mask, Blau_c = mask_producer(frame, mask_HSV, 'Blau')  # mask,(x,y,r,distanz)
    Grun_mask, Grun_c = mask_producer(frame, mask_HSV, 'Grun')

    """speicher die gefundene bälle in eine liste detected_Balls"""
    if Blau_c != []:#wenn es Blaue ball gibt
        detected_Balls = coordinat_zu_ordnen('Blau', Blau_c, detected_Balls)
    if Grun_c != []:#wenn es Grune ball gibt
        detected_Balls = coordinat_zu_ordnen('Grun', Grun_c, detected_Balls)

    cv2.imshow("Frame", frame)

    # if the 'q' key is pressed, stop the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break




temp_x = np.asarray(detected_Balls[0][0].x_coordinet)
temp_y = np.asarray(detected_Balls[0][0].y_coordinet)
temp_z = np.asarray(detected_Balls[0][0].distanc)

# close all windows
vs.stop()
cv2.destroyAllWindows()

# mpl.rcParams['legend.fontsize'] = 10
#
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# ax.plot(temp_x, temp_y, temp_z, label='parametric curve')
axes = plt.gca()
axes.set_xlim([-320,320])
axes.set_ylim([-240,240])
plt.plot(temp_x,temp_y,'o')
plt.show()