import time
import yaml

class DataProvider:
    def __init__(self):
        self.__stringTable = yaml.load(open('Strings.txt', 'r'))

    def GetStringTable(self, stringName):
        if stringName in self.__stringTable.keys():
            return self.__stringTable[stringName]
        else:
            return ''
