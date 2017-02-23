import serial
import time
ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(4)
counter = 10
while (counter > 0):
    ser.write('1/2/2/1/')
    ser.write('1/2/4/1/')
    time.sleep(1)
    ser.write('1/2/2/0/')
    ser.write('1/2/4/0/')
    time.sleep(1)
    counter = counter - 1
