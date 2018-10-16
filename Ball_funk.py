import cv2
import numpy as np
import matplotlib.pyplot as plt

hand_hist = None
traverse_point = []
total_rectangle = 9
hand_rect_one_x = None
hand_rect_one_y = None

hand_rect_two_x = None
hand_rect_two_y = None

Flag = None


def chek_x_y(frame):
    ''' if the Boll on the bordder of the image Flag on '''
    global hand_rect_one_x, hand_rect_one_y, Flag
    Flag = False
    rows, cols, _ = frame.shape

    if any(hand_rect_one_x < 10) or any(hand_rect_one_y < 10) or any(hand_rect_one_x > rows - 10) or any(
            hand_rect_one_y > cols - 10):
        Flag = True
    return Flag


def draw_rect(frame, is_ball_hist_created):
    rows, cols, _ = frame.shape
    global total_rectangle, hand_rect_one_x, hand_rect_one_y, hand_rect_two_x, hand_rect_two_y
    if not is_ball_hist_created:
        hand_rect_one_x = np.array(
            [8 * rows / 20, 8 * rows / 20, 8 * rows / 20, 9 * rows / 20, 9 * rows / 20, 9 * rows / 20, 10 * rows / 20,
             10 * rows / 20, 10 * rows / 20], dtype=np.uint32)

        hand_rect_one_y = np.array(
            [9 * cols / 25, 10 * cols / 25, 11 * cols / 25, 9 * cols / 25, 10 * cols / 25, 11 * cols / 25,
             9 * cols / 25,
             10 * cols / 25, 11 * cols / 25], dtype=np.uint32)

    hand_rect_two_x = hand_rect_one_x + 10
    hand_rect_two_y = hand_rect_one_y + 10

    print(rows, cols)
    print(hand_rect_one_y, rows)
    print(hand_rect_one_x, cols)
    for i in range(total_rectangle):
        cv2.rectangle(frame, (hand_rect_one_y[i], hand_rect_one_x[i]), (hand_rect_two_y[i], hand_rect_two_x[i]),
                      (0, 255, 0), 1)

    return frame


def draw_moving_rect(frame, x, y, r):
    global hand_rect_one_x, hand_rect_one_y
    rows, cols, _ = frame.shape
    li,re = 8,2
    hand_rect_one_x = np.array(
        [y - r / 2 - li, y - r / 2 - li, y - r / 2 - li, y - 5, y - 5, y - 5, y + r / 2 - re, y + r / 2 - re, y + r / 2 - re],
        dtype=np.uint32)

    hand_rect_one_y = np.array(
        [x - r / 2 - li, x - 5, x + r / 2 - re, x - r / 2 - li, x - 5, x + r / 2 - re, x - r / 2 - li, x - 5, x + r / 2 - re],
        dtype=np.uint32)


def hand_histogram(frame):
    global hand_rect_one_x, hand_rect_one_y

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi = np.zeros([90, 10, 3], dtype=hsv_frame.dtype)

    for i in range(total_rectangle):
        roi[i * 10: i * 10 + 10, 0: 10] = hsv_frame[hand_rect_one_x[i]:hand_rect_one_x[i] + 10,
                                          hand_rect_one_y[i]:hand_rect_one_y[i] + 10]

    hand_hist = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    data = np.zeros((3, 2))  # data = hsv min and max valus
    # data[0, 0] = np.amin(roi[:, :, 0])
    # data[0, 1] = np.amax(roi[:, :, 0])
    # data[1, 0] = np.amin(roi[:, :, 1])
    # data[1, 1] = np.amax(roi[:, :, 1])
    # data[2, 0] = np.amin(roi[:, :, 2])
    # data[2, 1] = np.amax(roi[:, :, 2])
    data[0, 0] = np.median(roi[:, :, 0] - 20)
    data[0, 1] = np.median(roi[:, :, 0] + 20)
    data[1, 0] = np.median(roi[:, :, 1] - 50)
    data[1, 1] = np.median(roi[:, :, 1] + 50)
    data[2, 0] = np.median(roi[:, :, 2] - 50)
    data[2, 1] = np.median(roi[:, :, 2] + 50)
    # print(data)
    return data
