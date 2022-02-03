"""!
@file main.py
Main file which runs a step response to rotate one revolution, prints values of 
time v.s. encoder position in ticks, and resets the system to run another
response. First, pins are created that will be used in the encoder/motor driver
and an encoder/motor object is created. The code then goes through a loop
asking the user for a Kp value, running the response by constantly updating
controller calculated duty and encoder position. After 2 seconds the encoder
is set to zero and all information collected in time/position arrays is
displayed. The user can exit the loop by pressing control+c, which will also
turn off the motor.
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
    ## Number of ticks per revolution of our motor
    ticks_per_rev = 256*2*16
    
    start = True
    
    # Setting up pins for motor and creating motor object
    pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    pinB4 = pyb.Pin(pyb.Pin.board.PB4)
    pinB5 = pyb.Pin(pyb.Pin.board.PB5)
    motor = motor_clephan_mcgrath.MotorDriver(pinA10, pinB4, pinB5, 3)
    
    # Setting up pins for encoder and creating encoder object
    pinC6 = pyb.Pin(pyb.Pin.board.PC6)
    pinC7 = pyb.Pin(pyb.Pin.board.PC7)
    encoder = encoder_clephan_mcgrath.Encoder(pinC6,pinC7,8)
    
    while True:
        try:
            if start:
                encoder.zero()
                #Asks for a proportional gain value from user
                Kp = float(input('Input a proportional gain value and press enter: '))
                print('Start')
                #Instantiates controller object with specified Kp
                controller = control.ClosedLoop([Kp,0,0], [-100,100], ticks_per_rev)
                #Starting time to collect data
                startTime = utime.ticks_ms()
                t_cur = utime.ticks_ms()
                start = False
            else:
                #Updates encoder position, uses that value to update duty from controller, and sleeps 10ms
                encoder.update()
                t_cur = utime.ticks_ms()
                duty = controller.update(encoder.read(), startTime)
                motor.set_duty_cycle(duty)
                utime.sleep_ms(10)
                
                #After 2 seconds from the start of the step response...
            if t_cur >= startTime+2000:
                #Printing out and resetting values for another step response
                start = True
                controller.i = True
                for n in range(len(controller.times)):
                    print("{:}, {:}".format(controller.times[n],controller.motorPositions[n]))
                controller.times = []
                controller.motorPositions = []
                startTime = utime.ticks_ms()
                encoder.zero()
                #Stop contiditon for user interface
                print('Stop')
        except KeyboardInterrupt:
            break
        
    motor.set_duty_cycle(0)
    print("\nProgram ending")
    
        