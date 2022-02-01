import pyb
import control
import utime
import encoder_clephan_mcgrath
import motor_clephan_mcgrath

if __name__ == "__main__":
    ticks_per_rev = 256*2*16
    curTicks = ticks_per_rev
    
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
                Kp = float(input('Input a proportional gain value and press enter: '))
                controller = control.ClosedLoop([Kp,0,0], [-100,100], curTicks)
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
            if t_cur >= startTime+1000:
                start = True
                controller.i = True
                curTicks+=ticks_per_rev
                controller.set_setPoint(curTicks)
                for n in range(len(controller.times)):
                    print("{:}, {:}".format(controller.times[n],controller.motorPositions[n]))
                controller.times = []
                startTime = utime.ticks_ms()
                motor.set_duty_cycle(0)
                print('Stop')
        except KeyboardInterrupt:
            break

#     print(controller.times)
#     print(controller.motorPositions)
    motor.set_duty_cycle(0)
    print("\nProgram ending")
    
        