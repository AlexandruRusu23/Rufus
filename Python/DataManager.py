import SerialManager
import DatabaseManager
import threading
import time
import datetime

class DataManager(threading.Thread):
    def __init__(self, serialName, serialRatio, databaseName):
        threading.Thread.__init__(self)
        self._runningLock = threading.Lock()
        self._serialManager = SerialManager.SerialManager(serialName, serialRatio)
        self._databaseManager = DatabaseManager.DatabaseManager(databaseName)
        self._isRunning = False
        self._threadLock = threading.Lock()

    def run(self):
        # Start the Serial Manager thread for reading
        self._serialManager.start()
        self._runningLock.acquire()
        self._isRunning = True
        self._runningLock.release()
        while(True):
            self.__StoreInDB()
            self._runningLock.acquire()
            if (self._isRunning == False):
                self._runningLock.release()
                break
            self._runningLock.release()

    def Stop(self):
        # Stop the Serial Manager thread
        self._serialManager.Stop()
        # Wait for the threads to stop
        self._serialManager.join()
        self._runningLock.acquire()
        self._isRunning = False
        self._runningLock.release()

    def GetData(self):
        return self._serialManager.GetScannerData()

    def __StoreInDB(self):
        # Store data from Serial into Database at every second
        dictScannerData = self._serialManager.GetScannerData()

        #we will use this data only for surveillance mode
        valuesList = [dictScannerData.get('distance'), dictScannerData.get('time_collected')]
        self._databaseManager.InsertDataInDatabase(valuesList, 'HOME_SCANNER_DATABASE_DISTANCE')

        valuesList = [dictScannerData.get('temperature'), dictScannerData.get('time_collected')]
        self._databaseManager.InsertDataInDatabase(valuesList, 'HOME_SCANNER_DATABASE_TEMPERATURE')

        valuesList = [dictScannerData.get('motion'), dictScannerData.get('time_collected')]
        self._databaseManager.InsertDataInDatabase(valuesList, 'HOME_SCANNER_DATABASE_MOTION')

        valuesList = [dictScannerData.get('humidity'), dictScannerData.get('time_collected')]
        self._databaseManager.InsertDataInDatabase(valuesList, 'HOME_SCANNER_DATABASE_HUMIDITY')

        valuesList = [dictScannerData.get('mq2'), dictScannerData.get('time_collected')]
        self._databaseManager.InsertDataInDatabase(valuesList, 'HOME_SCANNER_DATABASE_GAS_RECORD')

        valuesList = [dictScannerData.get('light'), dictScannerData.get('time_collected')]
        self._databaseManager.InsertDataInDatabase(valuesList, 'HOME_SCANNER_DATABASE_LIGHT')

        print "[DataManager] Incarc"
        time.sleep(0.5)
