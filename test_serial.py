import serial

ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyACM0'
ser.open()
for i in range(100):
    ser.flush()
    print(ser.read(2).decode('utf-8')[::-1])
ser.close()
