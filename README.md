# Lab 2 Step Response
## Christian Clephan, Kyle McGrath


![alt text](https://github.com/cclephan/Lab2/blob/main/TehFigure.png?raw=true)

Figure 1: Step Response at Kp = 0.03


This graph shows the proportional gain was not large enough because it only reached 8,000 ticks, 
where the setpoint is 1 revolution (8,192 ticks). The settling time occurs at about 300ms
and undershoots the set point by 200 ticks.

![alt text](https://github.com/cclephan/Lab2/blob/main/ElFigure.png?raw=true)

Figure 2: Step Response at Kp = 0.05


This graph shows the proportional gain was not large enough because it reached about 8,300, which 
is over the setpoint value. The settling time occurs slightly quicker with this Kp at about 270ms
and is off by about 100 ticks from the setpoint.

![alt text](https://github.com/cclephan/Lab2/blob/main/LeFigure.png?raw=true)

Figure 3: Step Response at Kp = 0.1


Increasing proportional gain again shows slight overshoot, but no oscillation or severe instability.
Although there was overshoot, the settling point and time was at 8,200 ticks and 350ms, which is extremely accurate, so
if the purposes of this motor was extreme accuracy regardless of overshoot or settling time this would be the best Kp.

![alt text](https://github.com/cclephan/Lab2/blob/main/ZeFigure.png?raw=true)

Figure 4: Step Response at Kp = 0.5

Setting proportional gain even higher shows larger overshoot and slight instability as the motor
oscillates around the setpoint value. The settling point and time is at 8,200 ticks and 550ms, but the
instability is not desireable in most circumstances.

When the proportional gain was set too large to be completely unstable and oscillations never stopped, the encoder would
not reset to zero. Instead the step response would begin at around double the setpoint value.
