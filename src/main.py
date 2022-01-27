import pyb
import control
import utime
import encoder_clephan_mcgrath
import motor_clephan_mcgrath

if __name__ == "__main__":
    ticks_per_rev = 256*2*16
    curTicks = ticks_per_rev
    
    controller = control.ClosedLoop([.5,0,0], [-100,100], curTicks)
    start = True
    pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    pinB4 = pyb.Pin(pyb.Pin.board.PB4)
    pinB5 = pyb.Pin(pyb.Pin.board.PB5)
    motor = motor_clephan_mcgrath.MotorDriver(pinA10, pinB4, pinB5, 3)
    
    pinC6 = pyb.Pin(pyb.Pin.board.PC6)
    pinC7 = pyb.Pin(pyb.Pin.board.PC7)
    encoder = encoder_clephan_mcgrath.Encoder(pinC6,pinC7,8)
    
    last_error = 0
    new_error = 1
    startTime = utime.ticks_ms()
    i = 0
    firstT = 0 
    while True:
        try:
            if start:
                input('Press enter to run step response')
                start = False
            else:
                #print(encoder.read())
                encoder.update()
                variables = controller.update(encoder.read(), startTime, firstT)
                if i == 0:
                    firstT = variables[3]
                    i = 1
                duty = variables[0]
                last_error = new_error
                new_error = variables[1]
                #print('Controlled duty ' + str(duty))
                motor.set_duty_cycle(duty)
                utime.sleep_ms(10)
            if new_error == last_error:
                last_error = 0
                new_error = 1
                start = True
                curTicks+=ticks_per_rev
                controller.set_setPoint(curTicks)
                for n in range(len(controller.times)):
                    print("{:}, {:}".format(controller.times[n],controller.motorPositions[n]))
                controller.times = []
                startTime = utime.ticks_ms()
        except KeyboardInterrupt:
            break

#     print(controller.times)
#     print(controller.motorPositions)
    motor.set_duty_cycle(0)
    print("\nProgram ending")
    
        