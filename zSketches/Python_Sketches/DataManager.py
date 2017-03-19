import SerialManager
import DatabaseManager

class DataManager:
    def __init__(self):
        self._serialManager = SerialManager.SerialManager('/dev/ttyACM0', 9600)
        self._databaseManager = DatabaseManager.DatabaseManager('test.db')

    def StoreInDB(self):
        self._databaseManager.CreateTable()
        while(True):
            dictToDB = self._serialManager.GetScannerData()
            self._databaseManager.InsertScannerData(dictToDB)
