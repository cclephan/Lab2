"""!
@file main.py
The main file that will create an Encoder Class and a Motor Driver 
@author Christian Clephan
@author Kyle McGrath
@date   02-Jan-2022
@copyright (c) 2022 released under CalPoly
"""

import pyb
import control
import utime
import encoder_clephan_mcgrath
import motor_clephan_mcgrath

if __name__ == "__main__":
    ticks_per_rev = 256*2*16
    
    start = True
    pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    pinB4 = pyb.Pin(pyb.Pin.board.PB4)
    pinB5 = pyb.Pin(pyb.Pin.board.PB5)
    motor = motor_clephan_mcgrath.MotorDriver(pinA10, pinB4, pinB5, 3)
    
    pinC6 = pyb.Pin(pyb.Pin.board.PC6)
    pinC7 = pyb.Pin(pyb.Pin.board.PC7)
    encoder = encoder_clephan_mcgrath.Encoder(pinC6,pinC7,8)
    
    while True:
        try:
            if start:
                encoder.zero()
                Kp = float(input('Input a proportional gain value and press enter: '))
                print('Start')
                controller = control.ClosedLoop([Kp,0,0], [-1000,1000], ticks_per_rev)
                startTime = utime.ticks_ms()
                t_cur = utime.ticks_ms()
                start = False
            else:
                #print(encoder.read())
                encoder.update()
                t_cur = utime.ticks_ms()
                duty = controller.update(encoder.read(), startTime)
                motor.set_duty_cycle(duty)
                utime.sleep_ms(10)
            if t_cur >= startTime+2000:
                #motor.set_duty_cycle(0)
                start = True
                controller.i = True
                for n in range(len(controller.times)):
                    print("{:}, {:}".format(controller.times[n],controller.motorPositions[n]))
                controller.times = []
                controller.motorPositions = []
                startTime = utime.ticks_ms()
                encoder.zero()
                print('Stop')
        except KeyboardInterrupt:
            break
        
    motor.set_duty_cycle(0)
    print("\nProgram ending")
    
        