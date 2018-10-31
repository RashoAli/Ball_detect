import cv2
import matplotlib.pyplot as plt
import numpy as np

Auto_position = None
Sigma = None


def g(state, control, w):
    x, y, theta = state
    l, r = control
    if l != r:
        alpha = (r - l) / w
        R = r / alpha
        g1 = x + (R + w / 2) * (np.sin(theta + alpha) - np.sin(theta))
        g2 = x + (R + w / 2) * (-np.cos(theta + alpha) + np.cos(theta))
        g3 = theta + alpha
    else:
        g1 = x + l * np.cos(theta)
        g2 = y + l * np.sin(theta)
        g3 = theta
    return np.array([g1, g2, g3])


def dg_dstate(state, control, w):
    theta = state[2]
    l, r = control
    if l != r:
        alpha = (r - l) / w
        R = r / alpha
        g1_theta = (R + w / 2) * (np.cos(theta + alpha) - np.cos(theta))
        g2_theta = (R + w / 2) * (np.sin(theta + alpha) - np.sin(theta))
    else:
        g1_theta = -l * np.sin(theta)
        g2_theta = l * np.cos(theta)

    G = np.array([1, 0, g1_theta], [0, 1, g2_theta], [0, 0, 1])
    return G


def dg_dcontrol(state, control, w):
    theta = state[2]
    l, r = control
    if l != r:
        alpha = (r - l) / w
        R = r / alpha
        theta_p = theta + alpha
        erst_term = w * r / ((r - l) * (r - l))
        g1_l = erst_term * (np.sin(theta_p) - np.sin(theta)) - (r + l) / (2 * (r - l)) * np.cos(theta_p)
        g2_l = erst_term * (-np.cos(theta_p) + np.cos(theta)) - (r + l) / (2 * (r - l)) * np.sin(theta_p)
        g3_l = -1 / w

        g1_r = -l / r * erst_term * (np.sin(theta_p) - np.sin(theta)) + (r + l) / (2 * (r - l)) * np.cos(theta_p)
        g2_r = -l / r * erst_term * (-np.cos(theta_p) + np.cos(theta)) + (r + l) / (2 * (r - l)) * np.sin(theta_p)
        g3_r = 1 / w
    else:
        g1_l = 0.5 * (np.cos(theta) + l * np.sin(theta) / w)
        g2_l = 0.5 * (np.sin(theta) - l * np.cos(theta) / w)
        g3_l = -1 / w

        g1_r = 0.5 * (- l * np.sin(theta) / w + np.cos(theta))
        g2_r = 0.5 * (l * np.cos(theta) / w + np.sin(theta))
        g3_r = -1 / w

    V = np.array([g1_l, g1_r], [g2_l, g2_r], [g3_l, g3_r])
    return V


def Extended_Kalman_filter():
    x = 0
    return x
