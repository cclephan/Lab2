import serial

with serial.Serial ('COM4', 115200) as s_port:
    s_port.write (b'something')

    print (s_port.readline ().split (b','))
