import serial

with serial.Serial ('COM4', 115200) as s_port:

    s_port.write(b'hello\n')

print(s_port.readline().split(b','))
