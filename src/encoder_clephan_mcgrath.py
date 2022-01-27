import pyb
import time
import motor_clephan_mcgrath

## Encoder period 
Encoder_Period = (2**16)

#Defines a class for our example FSM
class Encoder:
    ''' @brief                  Interface with quadrature encoders
        @details
    '''
    
    def __init__(self,Pinch1,Pinch2,timerNum):

        ''' 
        @brief Constructs an encoder object
        @details Instantiates timer, timer channels for encoder, and actual/encoderr position
        @param Pinch1 is the encoder channel B
        @param Pinch2 is the encoder channel A
        @param timerNum is timer number used as found on Nucleo datasheet
        
        '''

        ## @brief Configures Nucleo timer at some parameter timerNum, and
        self.timX = pyb.Timer(timerNum, prescaler=0, period=Encoder_Period-1)
        
        ## Configures relationship between timer and encoder B pin
        self.timX.channel(1, mode = pyb.Timer.ENC_B, pin=Pinch1)
        
        ## Configures relationship between timer and encoder A pin
        self.timX.channel(2, mode = pyb.Timer.ENC_A, pin=Pinch2)
        
        ## Actual position as recorded by the encoder
        self.position  = self.timX.counter();
        
        ## Encoder position, which doesn't account for overflow
        self.Eposition = self.timX.counter();
        
        print('Creating encoder object')

    def update(self):

        ''' 
        @brief              Updates encoder position and delta
        '''
        
        self.position = self.read() + self.get_delta()
        self.Eposition = self.timX.counter()
        
        
        #print('Reading encoder count and updating position and delta values')
        #print(self.position)
        
    def read(self):

        ''' @brief              Returns encoder position
            @return             The position of the encoder shaft
        '''
        return self.position

    def zero(self):

        ''' @brief              Sets encoder position to zero
        
        '''
        self.position = 0

    def get_delta(self):

        ''' @brief              Returns encoder delta
            @return             The change in position of the encoder shaft between the two most recent updates
        '''
        ## Change in position
        delp = self.timX.counter() - self.Eposition
        
        #Accounts for encoder overflow when values are negative or exceed 2^16-1
        if delp>Encoder_Period/2:
            return delp - Encoder_Period
        elif delp<-Encoder_Period/2:
            return delp + Encoder_Period
        
        return delp
    
    def __repr__(self):
        return "Encoder Position: " + str(self.position)

# 
# if __name__ == "__main__":
#     motor = motor_clephan_mcgrath.MotorDriver(pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP),pyb.Pin(pyb.Pin.board.PB4),pyb.Pin(pyb.Pin.board.PB5), 3)
#     motor.set_duty_cycle(40)
#     pinC6 = pyb.Pin(pyb.Pin.board.PC6)
#     pinC7 = pyb.Pin(pyb.Pin.board.PC7)
#     encoder = Encoder(pinC6,pinC7,8)
#     while True:
#         try:
#             encoder.update()
#             print(encoder.get_position())
#             
#         except KeyboardInterrupt():
#             break
#     print('Program End')
# #    