import serial
from matplotlib import pyplot

...
with serial.Serial ('COM4', 115200) as s_port:
    ...
    s_port.write (b'.5\r\n')   # Write bytes, not a string
    line = s_port.readline()
    time = []
    space = []
    while line != b'Stop\r\n':
        try:
            temp = line.split (b',')
            # print(temp)
            time.append(float(temp[0]))
            space.append(float(temp[1]))
        except:
            pass
        finally:
            line = s_port.readline()
    print("Do we get this far???")
    print(time) 
    print(space)
    pyplot.plot(time, space)
    pyplot.xlabel('Time (s)')
    pyplot.ylabel('Position (ticks)')
    pyplot.title('Step Impulse')
    pyplot.grid(True)
    pyplot.show()
    