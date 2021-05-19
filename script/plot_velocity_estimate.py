import numpy as np
import matplotlib.pyplot as plt

from src.robopi.script.velocity_estimation import trkloop
from src.robopi.script.velocity_estimation import sliding_average

US_TO_S = (1.0 / (1000.0 * 1000.0))
COUNT_TO_RAD = np.pi / 5.0
TICKS_US_TO_RAD_S = COUNT_TO_RAD / US_TO_S
data = np.genfromtxt('/home/phil/code/robopi_ws/src/robopi/data/log_loop.csv', delimiter=',',
                     skip_footer=10, names=True)
t = data['t_loop_us'] * US_TO_S
posLeft = data['pos_left_ticks'] * COUNT_TO_RAD
posRight = data['pos_right_ticks'] * COUNT_TO_RAD
dT = np.zeros_like(t)
for i in range(1, len(t)):
    dT[i] = t[i] - t[i - 1]

ki = 5
kp = 7.5
kd = 0.0
[estPosLeft, estVelLeft, estFilterVelLeft] = trkloop(posLeft, dT, kp=kp, ki=ki)
[estPosRight, estVelRight, estFilterVelRight] = trkloop(posRight, dT, kp=kp, ki=ki)
fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Loop")
ax1.set_xlabel('t [s]')
ax1.set_ylabel('pos')

ax1.plot(t, posLeft, label='pos left [ticks]')
ax1.plot(t, posRight, label='pos right [ticks]')

ax1.plot(t, estPosLeft, label='est pos left [ticks]')
ax1.plot(t, estPosRight, label='est pos right [ticks]')

leg = ax1.legend()

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Loop")
ax1.set_xlabel('t [s]')
ax1.set_ylabel('v')

windowSize = 1000
vLeftMean = sliding_average(posLeft, dT, windowSize)
vLeft = sliding_average(posLeft, dT, 1)
vRightMean = sliding_average(posRight, dT, windowSize)
vRight = sliding_average(posRight, dT, 1)


print("Sample time: {0:.6f} +- {1:.6f} s".format(np.mean(dT),np.std(dT)))
print("Sample time: {0:.6f} hz".format(1/np.mean(dT)))

log_target = np.genfromtxt('/home/phil/code/robopi_ws/src/robopi/data/log_velocity_filter.csv', delimiter=',',
                     skip_footer=10, names=True)

vLeftMeanTarget = data['v_left_mean_rads']
vLeftObsTarget = data['v_left_obs_rads']
vLeftMeanTargetUnit = log_target['v_avg_left_rads']
vLeftObsTargetUnit = log_target['v_obs_left_rads']


vRightObsTarget = data['v_right_obs_rads']
vRightMeanTarget = data['v_right_mean_rads']
vRightObsTargetUnit = log_target['v_obs_right_rads']
vRightMeanTargetUnit = log_target['v_avg_right_rads']

#ax1.plot(t, vLeft, label='v left [rad/s]')
ax1.plot(t, vLeftMean, label='v left mean [rad/s]')
ax1.plot(t, estVelLeft, label='v left trk [rad/s]')
ax1.plot(t, vLeftMeanTarget, label='v left mean target [rad/s]')
ax1.plot(t, vLeftObsTarget, label='v left trk target [rad/s]')
ax1.plot(t, vLeftObsTargetUnit, label='v left trk target unit [rad/s]')
leg = ax1.legend()

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Loop")
ax1.set_xlabel('t [s]')
ax1.set_ylabel('v')

#ax1.plot(t, vRight, label='v right [rad/s]')
ax1.plot(t, vRightMean, label='v right mean [rad/s]')
ax1.plot(t, vRightMeanTarget, label='v right mean target [rad/s]')
ax1.plot(t, vRightObsTarget, label='v right trk target [rad/s]')
ax1.plot(t, vRightObsTargetUnit, label='v right trk target unit [rad/s]')
ax1.plot(t, estVelRight, label='v right trk [rad/s]')


leg = ax1.legend()
plt.show()
