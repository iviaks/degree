import serial

ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyACM0'
ser.open()
for i in range(100):
    ser.flush()
    s = ''
    ch = ser.read()
    while ch != b'\n':
        s += ch.decode('utf-8')
        ch = ser.read()
    print(s)
ser.close()
