import MySQLdb
import time
import datetime
import UserDataProvider

class DatabaseManager:
    def __init__(self, databaseName):
        self._databaseName = databaseName
        self._dbConnection = MySQLdb.connect("localhost", "root", "internet12", self._databaseName)
        self.CreateTable()

    def Connect(self):
        self._dbConnection = MySQLdb.connect("localhost", "root", "internet12", self._databaseName)

    def Disconnect(self):
        self._dbConnection.close()

    def CreateTable(self):
        self.Connect()
        try:
            self._cursor = self._dbConnection.cursor();
            sqlCommand = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_TEMPERATURE
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            DOUBLE         NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self._cursor.execute(sqlCommand)

            sqlCommand = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_GAS_RECORD
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE_1          INT            NOT NULL,
                VALUE_2          INT            NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self._cursor.execute(sqlCommand)

            sqlCommand = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_LIGHT
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE_1          INT            NOT NULL,
                VALUE_2          INT            NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self._cursor.execute(sqlCommand)

            sqlCommand = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_HUMIDITY
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            DOUBLE         NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self._cursor.execute(sqlCommand)

            sqlCommand = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_MOTION
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            INT            NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self._cursor.execute(sqlCommand)

            sqlCommand = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_DISTANCE
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            DOUBLE         NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self._cursor.execute(sqlCommand)
        except:
            self._dbConnection.rollback()
            return 0
        self._dbConnection.close()

    def InsertDataInDatabase(self, valuesList, tableName):
        self.Connect()
        try:
            if valuesList[0] == None:
                return
            self._cursor = self._dbConnection.cursor()
            var_string = ', '.join(['%s'] * len(valuesList))
            if len(valuesList) == 2:
                query_string = "INSERT INTO %s (value, time_collected) VALUES (%s);" % (tableName, var_string)
            else:
                query_string = "INSERT INTO %s (value_1, value_2, time_collected) VALUES (%s);" % (tableName, var_string)
            self._cursor.execute(query_string, valuesList)
            self._dbConnection.commit()
        except TypeError as e:
            print e
            self._dbConnection.rollback()
        self._dbConnection.close()

    #select strftime('%Y - %m - %d', time_collected) from home_scanner_database;

    def GetDataFromDatabase(self, tableName):
        """
        Return a list with all records store in a specified table
        """
        self.Connect()
        self._cursor = self._dbConnection.cursor()
        query_string = 'SELECT * FROM %s' % tableName
        self._cursor.execute(query_string)
        valuesList = cursor.fetchall()
        self._dbConnection.close()
        return valuesList
