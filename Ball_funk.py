import cv2
import numpy as np
import imutils
from scipy import ndimage


class ObjektBall:
    """jeder ball Objekt"""

    def __init__(self):
        '''das bal würde schon einmal gesehen'''
        self.Flag = None
        '''' bestimung von position data'''
        self.x_coordinate = 0  # x auf die coordienatensystem
        self.y_coordinate = 0  # y auf die coordienatensystem
        self.x_image = 0  # x auf dem image
        self.y_image = 0  # y auf dem image
        self.radius = 0
        self.distance = 0


def mask_producer(mask_gray, mask_HSV, color):
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
        mask_gray_bllu = mask_gray[int(y) - int(r) - 10:int(y) + int(r) + 10,
                         int(x) - int(r) - 10:int(x) + int(r) + 10]
        print(np.shape(mask_gray_bllu))
        if all(np.shape(mask_gray_bllu)) != 0:
            ciecel_flag = circels(mask_gray_bllu)
            if ciecel_flag:
                cv2.circle(mask_gray, (int(x), int(y)), int(r),
                           (0, 255, 255), 2)
                cv2.circle(mask_gray, (int(x), int(y)), 5, (0, 0, 255), -1)
                centres.append((x, y, r))

    return mask_gray, centres


def circels(img):
    flag = False
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=255, param2=30, minRadius=0, maxRadius=0)
    if circles is not None:
        flag = True
    return flag

