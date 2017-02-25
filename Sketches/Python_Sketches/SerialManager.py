import serial
import time
import datetime
import re

class SerialManager:
    def __init__(self, serialName, serialRatio):
        self._serialFile = serial.Serial(serialName, serialRatio)
        self._isRunning = False
        self._listScannerCommands = []
        self._dictScannerData = {}

    def Start(self):
        self._isRunning = True

    def Stop(self):
        self._isRunning = False
        self._serialFile.close();

    def Reader(self):
        print('Serial reader function')
        while (self._isRunning):
            line = self._serialFile.readline()
            if('scanner_data' in line):
                line = self._serialFile.readline()
                while('end_scanner_data' not in line):
                    if(line):
                        self.StoreInDictionary(line)
                    line = self._serialFile.readline()
            self._dictScannerData['time_collected'] = datetime.datetime.now()
            #print self._dictScannerData

    def Writer(self):
        print('Serial writer function')
        for i in range(len(self._listScannerCommands)):
            self._serialFile.write(self._listScannerCommands[i])
            time.sleep(50.0 / 1000.0)
        self._listScannerCommands = []

    def GetScannerData(self, dictScannerData):
        dictScannerData.clear()
        dictScannerData = self._dictScannerData

    def SetScannerCommands(self, listScannerCommands):
        """
        send a list of commands for SerialManager to send to Microcontroller
        """
        self._listScannerCommands = []
        self._listScannerCommands = listScannerCommands

    def StoreInDictionary(self, lineToStore):
        lineToStoreTokenized = re.findall(r"[\w.]+", lineToStore)
        for i in range(len(lineToStoreTokenized)):
            if ('gas' in lineToStoreTokenized[i]):
                self._dictScannerData['mq2_1'] = lineToStoreTokenized[i+1]
                self._dictScannerData['mq2_2'] = lineToStoreTokenized[i+2]
                continue
            if ('temperature' in lineToStoreTokenized[i]):
                self._dictScannerData['temperature'] = lineToStoreTokenized[i+1]
                continue
            if ('light' in lineToStoreTokenized[i]):
                self._dictScannerData['light_1'] = lineToStoreTokenized[i+1]
                self._dictScannerData['light_2'] = lineToStoreTokenized[i+2]
                continue
            if ('humidity' in lineToStoreTokenized[i]):
                self._dictScannerData['humidity'] = lineToStoreTokenized[i+1]
                continue
            if ('distance' in lineToStoreTokenized[i]):
                self._dictScannerData['distance'] = lineToStoreTokenized[i+1]
                continue
            if ('motion' in lineToStoreTokenized[i]):
                self._dictScannerData['motion'] = lineToStoreTokenized[i+1]
                continue

"""
aux = SerialManager('/dev/ttyACM0', 9600)
aux.Start()
time.sleep(5)
print ("I'm connected to: " + aux._serialFile.name)
#aux.Writer()
aux.Reader()
"""
