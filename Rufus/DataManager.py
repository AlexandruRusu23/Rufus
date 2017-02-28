import SerialManager
import DatabaseManager
import threading
import time

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
        self._databaseManager.CreateTable()
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

    def __StoreInDB(self):
        # Store data from Serial into Database at every second
        dictScannerData = self._serialManager.GetScannerData()
        self._databaseManager.InsertScannerData(dictScannerData)
        time.sleep(1)
