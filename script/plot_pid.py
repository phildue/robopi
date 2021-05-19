import numpy as np
import matplotlib.pyplot as plt

US_TO_S = (1.0 / (1000.0 * 1000.0))
COUNT_TO_RAD = np.pi / 5.0
TICKS_US_TO_RAD_S = COUNT_TO_RAD / US_TO_S
data = np.genfromtxt('/home/phil/code/robopi_ws/src/robopi/data/log_pid.csv', delimiter=',',
                     skip_footer=10, names=True)
t = data['idx']*US_TO_S
posLeft = data['pos_left_ticks']*COUNT_TO_RAD
posRight = data['pos_right_ticks']*COUNT_TO_RAD
vLeftOnline = data['V_left_rads']
vRightOnline = data['V_right_rads']
vSet = data['V_rads']
errLeft = data['e_left_rads']
errRight = data['e_right_rads']
pwmLeft = data['pwm_left_']
pwmRight = data['pwm_right_']
dT = np.zeros_like(t)
for i in range(1, len(t)):
    dT[i] = t[i] - t[i - 1]


def trkloop(x, dt, kp, ki):
    velest = np.zeros_like(x)
    posest = np.zeros_like(x)
    velintegrator = np.zeros_like(x)

    for i in range(1, len(x)):
        posest[i] = posest[i-1] + velest[i-1]*dt[i-1]
        poserr = x[i]-posest[i]
        velintegrator[i] = velintegrator[i-1] + poserr*ki*dt[i]
        velest[i] = poserr * kp + velintegrator[i]

    return posest, velest, velintegrator


[estPosLeft, estVelLeft, estFilterVelLeft] = trkloop(posLeft, dT, kp=1.0, ki=0.07)
[estPosRight, estVelRight, estFilterVelRight] = trkloop(posRight, dT, kp=1.0, ki=0.07)
fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Loop")
ax1.set_xlabel('t [us]')
ax1.set_ylabel('pos')

iPosLeft = np.zeros_like(t)
iPosRight = np.zeros_like(t)

for i in range(1, len(t)):
    iPosLeft[i] = iPosLeft[i - 1] + vLeftOnline[i] * dT[i]
    iPosRight[i] = iPosRight[i - 1] + vRightOnline[i] * dT[i]

ax1.plot(t, posLeft, label='pos left [ticks]')
ax1.plot(t, posRight, label='pos right [ticks]')

ax1.plot(t, iPosLeft, label='ipos left [ticks]')
ax1.plot(t, iPosRight, label='ipos right [ticks]')

ax1.plot(t, estPosLeft, label='est pos left [ticks]')

leg = ax1.legend()

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Loop")
ax1.set_xlabel('t [us]')
ax1.set_ylabel('v')
dPosLeft = np.zeros_like(t)
dPosRight = np.zeros_like(t)

for i in range(1, len(t)):
    dPosLeft[i] = posLeft[i] - posLeft[i - 1]
    dPosRight[i] = posRight[i] - posRight[i - 1]
vLeft = dPosLeft / dT
vRight = dPosRight / dT

vLeftMean = np.zeros_like(vLeft)
vRightMean = np.zeros_like(vRight)
windowSize = 30
for i in range(windowSize, len(vLeftMean)):
    vLeftMean[i] = np.mean(vLeft[i - windowSize:i])
    vRightMean[i] = np.mean(vRight[i - windowSize:i])

# ax1.plot(t, vLeft, label='v left [rad/s]')
ax1.plot(t, vLeftOnline, label='v left~ [rad/s]')
#ax1.plot(t, vLeftMean, label='v left* [rad/s]')
#ax1.plot(t, estVelLeft, label='v left trk [rad/s]')
# ax1.plot(t, vRight, label='v right [rad/s]')
ax1.plot(t, vRightOnline, label='v right~ [rad/s]')
#ax1.plot(t, vRightMean, label='v right* [rad/s]')
#ax1.plot(t, estVelRight, label='v right trk [rad/s]')
ax1.plot(t, vSet, label='v set [rad/s]')
leg = ax1.legend()

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Loop")
ax1.set_xlabel('t [us]')
ax1.set_ylabel('err')
ax1.plot(t, errLeft, label='err left [rad/s]')
ax1.plot(t, errRight, label='err right [rad/s]')
leg = ax1.legend()

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Loop")
ax1.set_xlabel('t [us]')
ax1.set_ylabel('pwm')
ax1.plot(t, pwmLeft, label='pwm left [%]')
ax1.plot(t, pwmRight, label='pwm right [%]')
leg = ax1.legend()

plt.show()
