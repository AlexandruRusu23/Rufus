import SerialManager
import DatabaseManager
import threading
import time

class DataManagerThread (threading.Thread):
    def __init__(self, serialName, serialRatio, databaseName):
        threading.Thread.__init__(self)
        self._serialManager = SerialManager.SerialManager(serialName, serialRatio)
        self._databaseManager = DatabaseManager.DatabaseManager(databaseName)
        self._isRunning = False
        self._threadLock = threading.Lock()

    def __del__(self):
        self._serialManager.join()

    def Start(self):
        # Start the Serial Manager thread for reading
        self._serialManager.start()
        self._isRunning = True
        self.start()

    def Stop(self):
        # Stop the Serial Manager thread
        self._serialManager.Stop()
        # Wait for the threads to stop
        self._serialManager.join()
        self._isRunning = False

    def run(self):
        self._databaseManager.CreateTable()
        while(self._isRunning):
            self.__StoreInDB()

    def __StoreInDB(self):
        # Store data from Serial into Database at every second
        dictScannerData = self._serialManager.GetScannerData()
        self._databaseManager.InsertScannerData(dictScannerData)
        time.sleep(1)
