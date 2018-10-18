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


def mask_producer(frame, mask_HSV, color):
    mask = mask_HSV.copy()
    if color == 'Blau':
        blue_lower = (90, 40, 6)  # anfang werte fur die fabe
        blue_upper = (120, 255, 255)
        mask = cv2.inRange(mask, blue_lower, blue_upper)

    if color == 'Grun':
        green_lower = (40, 30, 10)  # anfang werte fur die fabe
        green_upper = (80, 255, 255)
        mask = cv2.inRange(mask, green_lower, green_upper)
        kernel = np.ones((20, 20), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    mask = cv2.erode(mask, None, iterations=5)
    mask = cv2.dilate(mask, None, iterations=5)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    centres = []
    for c in contours:
        # get the min area rect
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(frame, (int(x), int(y)), int(r),
                   (0, 255, 255), 2)
        cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
        centres.append((x, y, r))

    return mask, centres
