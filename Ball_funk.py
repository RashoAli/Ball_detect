import cv2
import numpy as np
import imutils
from scipy import ndimage

class ObjektBall:
    """jeder ball Objekt"""

    def __init__(self):
        '''das bal würde schon einmal gesehen'''
        self.color = ''
        '''' bestimung von position data'''
        self.x_coordinet = []  # x auf dem image
        self.y_coordinet = []  # y auf dem image


def mask_producer(frame, mask_HSV, color):
    mask = mask_HSV.copy()
    if color == 'Blau':
        blue_lower = (90, 40, 6)  # anfang werte fur die fabe
        blue_upper = (120, 255, 255)
        mask_range = cv2.inRange(mask, blue_lower, blue_upper)

    if color == 'Grun':
        green_lower = (40, 30, 10)  # anfang werte fur die fabe
        green_upper = (80, 255, 255)
        mask_range = cv2.inRange(mask, green_lower, green_upper)

    mask_range = cv2.erode(mask_range, None, iterations=5)
    mask_range = cv2.dilate(mask_range, None, iterations=5)
    _, contours, _ = cv2.findContours(mask_range, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    centres = []

    for c in contours:
        # get the min area rect
        ((x, y), r) = cv2.minEnclosingCircle(c)
        if r > 20:
            cv2.circle(frame, (int(x), int(y)), int(r),
                       (0, 255, 255), 2)
            cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
            Dictanc_Radius = 100000
            distenc = Dictanc_Radius / r
            centres.append((x, y, distenc))

    return mask_range, centres


def coordinat_zu_ordnen(col, center,detected_Balls):
    center = np.asarray(center)
    """camera geometri an geben"""
    alpha = 70  # in grad
    betha = 60
    """die coordienatn von den ball betimmen"""
    x = center[0,0]
    y = center[0,1]
    d = center[0,2]
    x_car = d * np.cos(np.deg2rad(alpha / (x - 240))) * np.cos(np.deg2rad(betha / (y - 320)))
    y_car = d * np.sin(np.deg2rad(alpha / (x - 240))) * np.sin(np.deg2rad(betha / (y - 320)))
    """neuer ball"""
    Ball = ObjektBall()
    Ball.color = col
    Ball.x_coordinet = x_car
    Ball.y_coordinet = y_car
    if not detected_Balls :  # das erdet detektierte ball
        detected_Balls.append((Ball, col))
        print(col,'new1')
    else:
        if any(col in s for s in detected_Balls):
            for boll in detected_Balls:
                if boll[1] == col:  # das ball ist schon in detected_Balls
                    boll[0].x_coordinet = np.append(boll[0].x_coordinet,x_car)
                    boll[0].y_coordinet = np.append(boll[0].y_coordinet,y_car)
        else :  # das ball ist noch nicht in detected_Balls
            print(col,'new2')
            detected_Balls.append((Ball, Ball.color))
    print(len(detected_Balls))
    return detected_Balls
