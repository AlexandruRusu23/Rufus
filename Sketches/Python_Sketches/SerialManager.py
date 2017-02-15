import serial
import time

class SerialManager:
    def __init__(self, serialName, serialRatio):
        self.serialFile = serial.Serial(serialName, serialRatio)
        self.isRunning = False
        self.commandList = ['1/2/5/100/', '1/2/6/100/', '1/2/9/255/', '2/1/0/', '1/2/5/0/', '1/2/6/0/', '1/2/9/0/']
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
aux.Writer()
aux.Reader()
