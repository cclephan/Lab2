import serial
from matplotlib import pyplot

Kp = input('Enter a Kp value: ')
b = bytes(Kp,'utf-8')+b'\r\n'

with serial.Serial ('COM4', 115200) as s_port:
    s_port.write (b)   # Write bytes, not a string
    line = s_port.readline()
    time = []
    space = []
    while not b'Stop' in line:
        try:
            temp = line.split (b',')
            #print(temp)
            time.append(float(temp[0]))
            space.append(float(temp[1]))
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
    print(time) 
    #print(space)
    pyplot.plot(time, space)
    pyplot.xlabel('Time (sec)')
    pyplot.ylabel('Position (ticks)')
    pyplot.title('Step Impulse')
    pyplot.grid(True)
    pyplot.show()
    print('Working')
    time = []
    space = []
    