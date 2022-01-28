# -*- coding: utf-8 -*-
import utime
"""
    @file closedloop.py
    @brief Closed loop controller containing methods to control an arbitraries motor duty cycle
    @details Controller uses the difference of reference and current values to create an error variable. PID gains, the time 
             difference, and magnitude of error are then used in the update method to return a duty for the motor to be run.
    @author Christian Clephan
    @author John Bennett
    @date   November 9, 2021

@author 
"""

class ClosedLoop:
    ''' @brief                  Interface with closed loop controller
        @details                Contains all methods that will be used in task_hardware to set the duty cycle based on closed
                                loop control.
    '''
        
    def __init__ (self,PID, satLim, setPoint):
        ''' @brief Constructs a closed loop controller
            @details Sets PID and saturation limits to what is determined by task_hardware and instantiates error variables.
            @param PID is a list containing the three gain values for Kp/Ki/Kd
            @param satLim is a list containing the upper and lower bounds of saturation      
        '''
        ## @brief Instantiates PID controller with gains
        self.firstTime = 0
        self.i = True
        self.PID = PID
        # PID Kp(*%/rad)Ki(*%/rad)Kd(*%s2/rad)
        ## @brief Instantiates duty saturation upper and lower bounds
        self.satLim = satLim
        
        self.setPoint = setPoint
        
        ## @brief Sum of error over a difference in time
        self.esum = 0
        ## @brief Previous error
        self.laste = 0
        self.times = []
        self.motorPositions = []
        #self.t0 = utime.ticks_ms()
        
        print("Controller Instantiated")

    def update (self, Read, startTime):
        ''' @brief Constructs a closed loop controller
            @details Sets PID and saturation limits to what is determined by task_hardware and instantiates error variables.
            @param PID is a list containing the three gain values for Kp/Ki/Kd
            @param satLim is a list containing the upper and lower bounds of saturation    
            @return Sends back saturated duty value using sat method.
        '''
        ## @brief Error signal which is the difference between a reference and input (current) value.
        e = self.setPoint - Read
        tcur = utime.ticks_ms()
        tdif = utime.ticks_diff(tcur,startTime)
        if self.i:
            self.firstTime = tdif
            self.i = False
        self.times.append(tdif-self.firstTime)
        self.motorPositions.append(Read)
        #Updates sum of error (area under curve)
        # self.esum += (self.laste+e)*tdif/2
        # ## @brief Delta error calculated by taking difference in error values over a time difference
        # dele = (e - self.laste)/tdif
        # # Updates last error
        # self.laste = e
        #print(e)

        
        ## @brief Duty calculation using PID gains and error values
        # duty = self.PID[0]*(e) + self.PID[1]*(self.esum) + self.PID[2]*(dele) 
        duty = self.PID[0]*(e)
        #print(self.motorPositions)
        return (self.sat(duty), e)
                
                
    def get_Times(self):
        return self.times
    
    def getPositions(self):
        return self.motorPositions
    
    def get_PID(self):
        ''' @brief Gets PID object
            @details Quick method to determine what controller is using for PID gains.     
        '''
        return self.PID
    
    def set_PID(self, PID):
        ''' @brief Sets PID gains.
            @details Sets PID gains to some new list of values for Kp/Ki/Kd 
            @param PID is a list containing the three gain values for Kp/Ki/Kd    
        '''
        self.PID = PID
        
    def set_setPoint(self,setPoint):
        
        self.setPoint = setPoint
        
    def sat(self,sat_duty):
        ''' @brief Saturation functionallity
            @details Controls if a duty is too large from what is calculated in update method.
            @param sat_duty is the value sent by what is calculated in update method.
            @return Sends back either the saturated limit if duty is too high or original duty based on bounds.
        '''
        if sat_duty<self.satLim[0]:
            return self.satLim[0]
        elif sat_duty>self.satLim[1]:
            return self.satLim[1]
        return sat_duty
      
