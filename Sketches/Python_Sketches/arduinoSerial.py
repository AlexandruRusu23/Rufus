import serial
import time
ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(4)
counter = 10
while (counter > 0):
    ser.write('1/2/7/0/')
    ser.write('1/2/5/1/')
    time.sleep(1)
    ser.write('1/2/5/0/')
    ser.write('1/2/6/1/')
    time.sleep(1)
    ser.write('1/2/6/0/')
    ser.write('1/2/7/1/')
    time.sleep(1)
    counter = counter - 1
