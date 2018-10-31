import cv2
import numpy as np
from skimage import color, data, restoration
from scipy.signal import convolve2d


class ObjektBall:
    """jeder ball Objekt"""

    def __init__(self):
        '''das bal würde schon einmal gesehen'''
        self.color = ''
        '''' bestimung von position data'''
        self.x_coordinet = []  # x auf dem image
        self.y_coordinet = []  # y auf dem image
        self.distanc = []
        self.frame = []


def mask_producer(frame, mask_HSV, color, frame_number):
    """ konstant"""
    Dictanc_Radius = 20000  # abstand zu radius

    """"""
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
    data = []  # alle (x_pixel,y_pixel,r) werden hier geschpeichert
    for c in contours:
        # get the min area rect
        ((x_pixel, y_pixel), r) = cv2.minEnclosingCircle(c)
        if r > 35:
            cv2.circle(frame, (int(x_pixel), int(y_pixel)), int(r),
                       (0, 255, 255), 2)
            cv2.circle(frame, (int(x_pixel), int(y_pixel)), 5, (0, 0, 255), -1)
            distenc = Dictanc_Radius / r
            data.append((x_pixel, y_pixel, distenc, frame_number))

    return mask_range, data


def coordinat_zu_ordnen(col, center, detected_Balls):
    center = np.asarray(center)
    """camera geometri an geben"""
    alpha = 70  # in grad
    betha = 60

    """die coordienatn von den ball zu das Auto betimmen"""
    x = center[0, 0] - 320
    y = center[0, 1] - 240
    d = center[0, 2]
    f = center[0, 3]

    x_boll_car = d * np.cos(np.deg2rad(alpha / x)) * np.cos(np.deg2rad(betha / y))
    y_boll_car = d * np.sin(np.deg2rad(alpha / x)) * np.cos(np.deg2rad(betha / y))

    """neuer ball"""
    Ball = ObjektBall()
    Ball.color = col
    Ball.x_coordinet = x_boll_car
    Ball.y_coordinet = y_boll_car
    Ball.distanc = d
    Ball.frame = f
    if not detected_Balls:  # das erset detektierte ball
        detected_Balls.append((Ball, col))
        print(col, 'new1')
    else:
        if any(col in s for s in detected_Balls):
            for boll in detected_Balls:
                if boll[1] == col:  # das ball ist schon in detected_Balls
                    boll[0].x_coordinet = np.append(boll[0].x_coordinet, x_boll_car)
                    boll[0].y_coordinet = np.append(boll[0].y_coordinet, y_boll_car)
                    boll[0].distanc = np.append(boll[0].distanc, d)
                    boll[0].frame = np.append(boll[0].frame, f)
        else:  # das ball ist noch nicht in detected_Balls
            print(col, 'new2')
            detected_Balls.append((Ball, Ball.color))
    return detected_Balls


def mask_auf_image(img, mask):
    """ gibt image nur da wo mask != 0"""
    img_array = np.asarray(img)
    mask_array = np.asarray(mask)
    img_array[:, :, 0][mask_array == 0] = 0
    img_array[:, :, 1][mask_array == 0] = 0
    img_array[:, :, 2][mask_array == 0] = 0
    return img_array
