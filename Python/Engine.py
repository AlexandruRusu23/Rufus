import DataProvider
import os
import yaml

class Engine:

    dataProvider = DataProvider.DataProvider() #static

    def __init__(self):
        self._arduinoBoards = []

    def ClearData(self):
        self._arduinoBoards = []

    def FindAllDevices(self):
        self.ClearData()
        filesToSearchIn = os.listdir(Engine.dataProvider.GetStringTable('PATH_ARDUINO_BOARDS'))
        fileSubstr = Engine.dataProvider.GetStringTable('SUBSTR_ARDUINO_FILE')
        for file in filesToSearchIn:
            if fileSubstr in file:
                self._arduinoBoards.append(file)

        print self._arduinoBoards
