import serial
import time

class SerialManager:
    def __init__(self, serialName, serialRatio):
        self.serialFile = serial.Serial(serialName, serialRatio)
        self.isRunning = False
        self.commandList = ['1/1/9/100/', '1/1/9/0/', '1/1/10/100/', '1/1/10/0/', '1/1/11/100/', '1/1/11/0/']
        self.dataDict = {}

    def Start(self):
        self.isRunning = True

    def Stop(self):
        self.isRunning = False
        self.serialFile.close();

    def Reader(self):
        print('Serial reader function')
        while (self.isRunning):
            line = self.serialFile.readline()
            if line:
                print(line)

    def Writer(self):
        print('Serial writer function')
        for i in range(len(self.commandList)):
            self.serialFile.write(self.commandList[i])
            time.sleep(1)

aux = SerialManager('/dev/ttyACM0', 9600)
aux.Start()
print ("I'm connected to: " + aux.serialFile.name)
time.sleep(5)
aux.Writer()
aux.Reader()
