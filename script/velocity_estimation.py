import numpy as np


def trkloop(x, dt, kp, ki, kd=0.0):
    velest = np.zeros_like(x)
    posest = np.zeros_like(x)
    poserr = np.zeros_like(x)
    velintegrator = np.zeros_like(x)

    for i in range(1, len(x)):
        posest[i] = posest[i - 1] + velest[i - 1] * dt[i - 1]
        poserr[i] = x[i] - posest[i]
        velintegrator[i] = velintegrator[i - 1] + ki * poserr[i] * dt[i]
        velest[i] = poserr[i] * kp + velintegrator[i] + kd * (poserr[i] - poserr[i - 1]) / dt[i]

    return posest, velest, velintegrator


def sliding_average(x, dt, window_size):
    v_window = np.zeros((window_size,))
    v_avg = np.zeros_like(x)
    for i in range(1,x.shape[0]):
        v = (x[i] - x[i - 1]) / dt[i]
        v_window[i % window_size] = v
        v_avg[i] = np.mean(v_window)
    return v_avg
