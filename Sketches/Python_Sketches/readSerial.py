import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

print("connected to: " + ser.name + '\n')

line = ""

while True:
    line = ser.readline()
    if line:
        print(line)
    if not line.strip():
        break

ser.close()
