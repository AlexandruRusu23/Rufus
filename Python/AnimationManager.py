import DatabaseManager
import SerialManager
import threading
import time
import datetime
import serial

class AnimationManager(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self._serialManager = serial.Serial('/dev/ttyUSB0', 9600)
        self._alarmOn = False
        self._threadLock = threading.Lock()
        self._runningLock = threading.Lock()
        self._serialLock = threading.Lock()
        self._isRunning = True

    def run(self):
        time.sleep(0.5)
        self.__StartupEffect()
        while True:
            self._runningLock.acquire()
            if self._isRunning == False:
                self._runningLock.release()
                break
            self._runningLock.release()

            self.__AlarmEffect()
            time.sleep(1)

    def Stop(self):
        self._runningLock.acquire()
        self._isRunning = False
        self._runningLock.release()
        self.StopTheAlarm()

    def __LightOneColor(self, colorStr, intensity):
        colorInt = 9 #blue by default
        if colorStr == 'red':
            colorInt = 11
        if colorStr == 'green':
            colorInt = 10
        self._serialLock.acquire()
        self._serialManager.write('1/1/' + str(colorInt) + '/' + str(intensity)+ '/')
        self._serialLock.release()
        time.sleep(0.2)

    def __LightModeColor(self, colorStr, intensity):
        colorInt = 2 #green mode by default
        if colorStr == 'yellow':
            colorInt = 3
        if colorStr == 'red':
            colorInt = 4
        if colorStr == 'blue':
            colorInt = 5
        self._serialLock.acquire()
        self._serialManager.write('1/2/' + str(colorInt) + '/' + str(intensity)+ '/')
        self._serialLock.release()
        time.sleep(0.2)

    def __StartupEffect(self):
        contor = 5
        while True:
            contor = contor - 1
            if contor < 0:
                break

            self.__LightModeColor('red', 1)
            self.__LightOneColor('red', 255)
            self.__LightModeColor('blue', 1)
            self.__LightOneColor('red', 0)
            self.__LightOneColor('green', 255)
            self.__LightModeColor('blue', 0)
            self.__LightModeColor('red', 0)
            self.__LightModeColor('yellow', 1)
            self.__LightOneColor('green', 0)
            self.__LightOneColor('blue', 255)
            self.__LightModeColor('green', 1)
            self.__LightOneColor('blue', 0)
            self.__LightModeColor('yellow', 0)
            self.__LightModeColor('green', 0)

    def __AlarmEffect(self):
        while True:
            self._threadLock.acquire()
            if self._alarmOn == False:
                self._threadLock.release()
                break
            self._threadLock.release()
            self.__LightOneColor('red', 255)
            self.__LightOneColor('red', 0)

    def RingTheAlarm(self):
        self._threadLock.acquire()
        self._alarmOn = True
        self._threadLock.release()

    def StopTheAlarm(self):
        self._threadLock.acquire()
        self._alarmOn = False
        self._threadLock.release()

    def TurnOnTheMode(self, modeColor):
        self.__LightModeColor(modeColor, 1)

    def TurnOffTheMode(self, modeColor):
        self.__LightModeColor(modeColor, 0)
