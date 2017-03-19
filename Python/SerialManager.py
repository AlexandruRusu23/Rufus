import threading
import serial
import time
import datetime
import re

class SerialManager(threading.Thread):
    """
    Class implemented to manipulate the Microcontroller's Serial
    """
    def __init__(self, serialName, serialRatio):
        """
        Serial Manager Constructor Args: serial name, serial ratio ('/dev/ttyACM0', 9600)
        """
        threading.Thread.__init__(self)
        self._runningLock = threading.Lock()
        self._scannerDictLock = threading.Lock()
        self.__serialFile = serial.Serial(serialName, serialRatio)
        self.__listScannerCommands = []
        self.__dictScannerData = {}
        self._isRunning = False

    def run(self):
        self._runningLock.acquire()
        self._isRunning = True
        self._runningLock.release()
        while(True):
            self.__Reader()

            self._runningLock.acquire()
            if(self._isRunning == False):
                self._runningLock.release()
                break
            self._runningLock.release()
        self.__serialFile.close();

    def __Reader(self):
        """
        Method created to read from Microcontroller's Serial
        """
        line = self.__serialFile.readline()
        if(line):
            if('scanner_data' in line):
                line = self.__serialFile.readline()
                while('end_scanner_data' not in line):
                    if(line):
                        self.__StoreInDictionary(line)
                    line = self.__serialFile.readline()
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            self._scannerDictLock.acquire()
            self.__dictScannerData['time_collected'] = timestamp
            self._scannerDictLock.release()

    def __StoreInDictionary(self, lineToStore):
        """
        Convert from string to dictionary fields
        """

        lineToStoreTokenized = re.findall(r"[\w.]+", lineToStore)
        for i in range(len(lineToStoreTokenized)):
            if ('gas' in lineToStoreTokenized[i]):
                self._scannerDictLock.acquire()
                self.__dictScannerData['mq2_1'] = lineToStoreTokenized[i+1]
                self.__dictScannerData['mq2_2'] = lineToStoreTokenized[i+2]
                self._scannerDictLock.release()
                continue
            if ('temperature' in lineToStoreTokenized[i]):
                self._scannerDictLock.acquire()
                self.__dictScannerData['temperature'] = lineToStoreTokenized[i+1]
                self._scannerDictLock.release()
                continue
            if ('light' in lineToStoreTokenized[i]):
                self._scannerDictLock.acquire()
                self.__dictScannerData['light_1'] = lineToStoreTokenized[i+1]
                self.__dictScannerData['light_2'] = lineToStoreTokenized[i+2]
                self._scannerDictLock.release()
                continue
            if ('humidity' in lineToStoreTokenized[i]):
                self._scannerDictLock.acquire()
                self.__dictScannerData['humidity'] = lineToStoreTokenized[i+1]
                self._scannerDictLock.release()
                continue
            if ('distance' in lineToStoreTokenized[i]):
                self._scannerDictLock.acquire()
                self.__dictScannerData['distance'] = lineToStoreTokenized[i+1]
                self._scannerDictLock.release()
                continue
            if ('motion' in lineToStoreTokenized[i]):
                self._scannerDictLock.acquire()
                self.__dictScannerData['motion'] = lineToStoreTokenized[i+1]
                self._scannerDictLock.release()
                continue

    def __Writer(self):
        """
        Method created to write on Microcontroller's Serial
        """
        for i in range(len(self.__listScannerCommands)):
            self.__serialFile.write(self.__listScannerCommands[i])
            time.sleep(50.0 / 1000.0)
        self.__listScannerCommands = []

    def Stop(self):
        """
        Stop the Serial Manager
        """
        self._runningLock.acquire()
        self._isRunning = False
        self._runningLock.release()

    def GetScannerData(self):
        """
        Get the data from Serial from a dictionary which is returned by the function
        """
        self._scannerDictLock.acquire()
        output = self.__dictScannerData
        self._scannerDictLock.release()
        return output

    def SetScannerCommands(self, listScannerCommands):
        """
        send a list of commands for SerialManager to be send to Microcontroller
        """
        self.__listScannerCommands = listScannerCommands

    def ExecuteCommands(self):
        """
        Send to Microcontroller's Serial the commands stored in __listScannerCommands
        """
        self.__Writer()
