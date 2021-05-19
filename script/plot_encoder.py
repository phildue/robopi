import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('/home/phil/code/robopi_ws/src/robopi/data/log_motor.csv', delimiter=',',
                     skip_footer=10, names=True)

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Velocity")
ax1.set_xlabel('tick')
ax1.set_ylabel('velocity')
idx = data['idx']
subIdx = 1
idx = idx[::subIdx]


def helper(coloumn):
    coloumn = coloumn[::subIdx]
    dt = np.zeros_like(coloumn)
    for i in range(subIdx, len(coloumn)):
        dt[i] = coloumn[i] - coloumn[i - subIdx]
    dt /= 1000 * 1000
    v = ((subIdx / dt) * np.pi / 5) / (2 * np.pi)

    mean_dt = np.zeros_like(dt)
    mean_v = np.zeros_like(dt)
    windowSize = 20
    for i in range(windowSize, len(dt)):
        mean_dt[i] = np.mean(dt[i - windowSize:i])
        mean_v[i] = np.mean(v[i - windowSize:i])
    return mean_v, v


t_gpio_left = data['t_gpio_left_us']
t_gpio_right = data['t_gpio_right_us']
mean_v_left, v_left = helper(t_gpio_left)
mean_v_right, v_right = helper(t_gpio_right)

#ax1.plot(idx, v_left, label='v left [round/s]')
ax1.plot(idx, mean_v_left, label='mean_v left [s]')
#ax1.plot(idx, v_right, label='v right [round/s]')
ax1.plot(idx, mean_v_right, label='mean_v right [s]')
leg = ax1.legend()

idx = data['idx']
t_chrono_left = data['t_chrono_left_us']
t_chrono_right = data['t_chrono_right_us']

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Velocity")
ax1.set_xlabel('idx')
ax1.set_ylabel('t')
ax1.plot(idx, t_chrono_left - t_chrono_left[0], label="t_chrono_left [us]")
ax1.plot(idx, t_chrono_right - t_chrono_right[0], label="t_chrono_right [us]")
#ax1.plot(idx, t_gpio_left - t_gpio_left[0], label="t_gpio_left [us]")
#ax1.plot(idx, t_gpio_right - t_gpio_right[0], label="t_gpio_right [us]")
leg = ax1.legend()

plt.show()
