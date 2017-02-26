import sqlite3
import time
import datetime

class DatabaseManager:
    def __init__(self, databaseName):
        self._databaseName = databaseName

    def Connect(self):
        try:
            self._connection = sqlite3.connect(self._databaseName)
        except:
            return 0
        self.CreateTable()

    def Disconnect(self):
        self._connection.close()

    def CreateTable(self):
        self.Connect()
        try:
            self._connection.execute('''CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE
                (ID              INTEGER     PRIMARY KEY AUTOINCREMENT        NOT NULL,
                MQ2_1            INTEGER     NOT NULL,
                MQ2_2            INTEGER     NOT NULL,
                LIGHT_1          INTEGER     NOT NULL,
                LIGHT_2          INTEGER     NOT NULL,
                TEMPERATURE      REAL        NOT NULL,
                HUMIDITY         INTEGER     NOT NULL,
                MOTION           INTEGER     NOT NULL,
                DISTANCE         REAL        NOT NULL,
                TIME_COLLECTED   DATE        NOT NULL);''')
        except:
            return 0

    def InsertScannerData(self, dictScannerData):
        self.Connect()
        try:
            self._connection.execute("INSERT INTO HOME_SCANNER_DATABASE (MQ2_1,MQ2_2,LIGHT_1,LIGHT_2, \
                TEMPERATURE,HUMIDITY,MOTION,DISTANCE,TIME_COLLECTED) VALUES \
                (:mq2_1, :mq2_2, :light_1, :light_2, :temperature, :humidity, :motion, \
                :distance, :time_collected);", dictScannerData)

            self._connection.commit()
        except:
            return 0

    #select strftime('%Y - %m - %d', time_collected) from home_scanner_database;

    def GetScannerData(self):
        self.Connect()
        cursor = self._connection.execute("SELECT MQ2_1, MQ2_2, LIGHT_1, LIGHT_2, TEMPERATURE, HUMIDITY, MOTION, DISTANCE, TIME_COLLECTED FROM HOME_SCANNER_DATABASE")
        auxDict = {}
        matDictScannerData = []
        for row in cursor:
            auxDict['mq2_1'] = row[0]
            auxDict['mq2_2'] = row[1]
            auxDict['light_1'] = row[2]
            auxDict['light_1'] = row[3]
            auxDict['temperature'] = row[4]
            auxDict['humidity'] = row[5]
            auxDict['motion'] = row[6]
            auxDict['distance'] = row[7]
            auxDict['time_collected'] = row[8]
            matDictScannerData.append(auxDict)
        return matDictScannerData
