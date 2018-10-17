import cv2
import numpy as np


class Ball_objekt():
    def __init__(self):
        self.traverse_point = []
        self.total_rectangle = 9
        self.hand_rect_one_x = None
        self.hand_rect_one_y = None

        self.hand_rect_two_x = None
        self.hand_rect_two_y = None

        self.Flag = None

    def chek_x_y(self, frame):
        ''' if the Boll on the bordder of the image Flag on '''
        self.Flag = False
        rows, cols, _ = frame.shape

        if any(self.hand_rect_one_x < 10) or any(self.hand_rect_one_y < 10) or any(
                self.hand_rect_one_x > rows - 10) or any(
            self.hand_rect_one_y > cols - 10):
            self.Flag = True
        return self.Flag

    def draw_rect(self, frame, is_ball_hist_created):
        rows, cols, _ = frame.shape
        if not is_ball_hist_created:
            self.hand_rect_one_x = np.array(
                [8 * rows / 20, 8 * rows / 20, 8 * rows / 20, 9 * rows / 20, 9 * rows / 20, 9 * rows / 20,
                 10 * rows / 20,
                 10 * rows / 20, 10 * rows / 20], dtype=np.uint32)

            self.hand_rect_one_y = np.array(
                [9 * cols / 25, 10 * cols / 25, 11 * cols / 25, 9 * cols / 25, 10 * cols / 25, 11 * cols / 25,
                 9 * cols / 25,
                 10 * cols / 25, 11 * cols / 25], dtype=np.uint32)

        self.hand_rect_two_x = self.hand_rect_one_x + 10
        self.hand_rect_two_y = self.hand_rect_one_y + 10

        for i in range(self.total_rectangle):
            cv2.rectangle(frame, (self.hand_rect_one_y[i], self.hand_rect_one_x[i]),
                          (self.hand_rect_two_y[i], self.hand_rect_two_x[i]),
                          (0, 255, 0), 1)

        return frame

    def draw_moving_rect(self, frame, x, y, r):
        rows, cols, _ = frame.shape
        li, re = 8, 2
        self.hand_rect_one_x = np.array(
            [y - r / 2 - li, y - r / 2 - li, y - r / 2 - li, y - 5, y - 5, y - 5, y + r / 2 - re, y + r / 2 - re,
             y + r / 2 - re],
            dtype=np.uint32)

        self.hand_rect_one_y = np.array(
            [x - r / 2 - li, x - 5, x + r / 2 - re, x - r / 2 - li, x - 5, x + r / 2 - re, x - r / 2 - li, x - 5,
             x + r / 2 - re],
            dtype=np.uint32)

    def hand_histogram(self, frame):

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        roi = np.zeros([90, 10, 3], dtype=hsv_frame.dtype)

        for i in range(self.total_rectangle):
            roi[i * 10: i * 10 + 10, 0: 10] = hsv_frame[self.hand_rect_one_x[i]:self.hand_rect_one_x[i] + 10,
                                              self.hand_rect_one_y[i]:self.hand_rect_one_y[i] + 10]

        data = np.zeros((3, 2))  # data = hsv min and max valus

        data[0, 0] = np.median(roi[:, :, 0] - 20)
        data[0, 1] = np.median(roi[:, :, 0] + 20)
        data[1, 0] = np.median(roi[:, :, 1] - 50)
        data[1, 1] = np.median(roi[:, :, 1] + 50)
        data[2, 0] = np.median(roi[:, :, 2] - 50)
        data[2, 1] = np.median(roi[:, :, 2] + 50)
        # print(data)
        return data
