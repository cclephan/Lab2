"""!
@file user_interface.py
This file contains the user interface which will run on the PC and send serial
input to the Nucleo and read back serial output. The user inputs a Kp value,
the motor will spin for 1 revolution, after 2 seconds, the user will be 
prompted again for another step response. This can be repeated unitil the user
presses control+c to stop the code.
@author Christian Clephan
@author Kyle McGrath
@date   02-Jan-2022
@copyright (c) 2022 released under CalPoly
"""

import serial
from matplotlib import pyplot


Kp = input('Enter a Kp value: ')
b = bytes(Kp,'utf-8')+b'\r\n'

with serial.Serial ('COM4', 115200) as s_port:
    #Sends Kp value to Nucleo for main.py Kp input
    s_port.write (b)
    line = s_port.readline()
    time = []
    position = []
    #Reads through lines of main.py from Nucleo until it finds Stop
    while not b'Stop' in line:
        try:
            temp = line.split (b',')
            #Appends to time and position lists
            time.append(float(temp[0]))
            position.append(float(temp[1]))
        except IndexError as error:
            print(error, line)
            #print(line)
            pass
        except ValueError as error:
            print(error, line)
        finally:
            line = s_port.readline()
    if time[0] != 0:
        time.pop(0)
    #Plots information collected in step response
    pyplot.plot(time, position)
    pyplot.xlabel('Time (ms)')
    pyplot.ylabel('Position (ticks)')
    pyplot.title('Step Impulse at Kp='+Kp)
    pyplot.grid(True)
    pyplot.show()
    time = []
    position = []
    