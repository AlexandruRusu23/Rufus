import DatabaseManager
import SerialManager
import DataProvider
import threading
import time
import datetime
import serial

class AnimationManager(threading.Thread):

    dataProvider = DataProvider.DataProvider() #static

    def __init__(self):
        threading.Thread.__init__(self)
        self.__serialManager = serial.Serial('/dev/ttyUSB0', 9600)
        self.__alarmOn = False
        self.__threadLock = threading.Lock()
        self.__runningLock = threading.Lock()
        self.__serialLock = threading.Lock()
        self.__isRunning = True
        self.__mainAnimOn = False
        self.__turnOff = False

    def run(self):
        time.sleep(0.5)
        self.__StartupEffect()
        while True:
            self.__runningLock.acquire()
            if self.__isRunning == False:
                self.__runningLock.release()
                break
            self.__runningLock.release()
            self.__MainAnimation()
            self.__AlarmEffect()
            time.sleep(1)

    def Stop(self):
        self.__runningLock.acquire()
        self.__isRunning = False
        self.__runningLock.release()
        self.StopTheAlarm()
        self.__TurnAllOff()

    def __LightOneColor(self, colorStr, intensity, timeout):
        colorInt = 11 #blue by default
        if colorStr == 'red':
            colorInt = 9
        if colorStr == 'green':
            colorInt = 10
        self.__serialLock.acquire()
        self.__serialManager.write(AnimationManager.dataProvider.GetStringTable('ANALOG_WRITE') + str(colorInt) + '/' + str(intensity)+ '/')
        self.__serialLock.release()
        time.sleep(timeout)

    def __LightModeColor(self, colorStr, intensity, timeout):
        colorInt = 2 #green mode by default
        if colorStr == 'yellow':
            colorInt = 3
        if colorStr == 'red':
            colorInt = 4
        if colorStr == 'blue':
            colorInt = 5
        self.__serialLock.acquire()
        self.__serialManager.write(AnimationManager.dataProvider.GetStringTable('DIGITAL_WRITE') + str(colorInt) + '/' + str(intensity)+ '/')
        self.__serialLock.release()
        time.sleep(0.2)

    def __TurnAllOff(self):
        if self.__turnOff == False:
            self.__turnOff = True
            self.__mainAnimOn = False
            self.__LightOneColor('red', 0, 0.1)
            self.__LightModeColor('blue', 0, 0.1)
            self.__LightModeColor('red', 0, 0.1)
            self.__LightOneColor('green', 0, 0.1)
            self.__LightOneColor('blue', 0, 0.1)
            self.__LightModeColor('yellow', 0, 0.1)
            self.__LightModeColor('green', 0, 0.1)

    def __StartupEffect(self):
        contor = 5
        while contor > 0:
            contor = contor - 1

            self.__LightModeColor('red', 1, 0.1)
            self.__LightOneColor('red', 255, 0.1)
            self.__LightModeColor('blue', 1, 0.1)
            self.__LightOneColor('red', 0, 0.1)
            self.__LightOneColor('green', 255, 0.1)
            self.__LightModeColor('blue', 0, 0.1)
            self.__LightModeColor('red', 0, 0.1)
            self.__LightModeColor('yellow', 1, 0.1)
            self.__LightOneColor('green', 0, 0.1)
            self.__LightOneColor('blue', 255, 0.1)
            self.__LightModeColor('green', 1, 0.1)
            self.__LightOneColor('blue', 0, 0.1)
            self.__LightModeColor('yellow', 0, 0.1)
            self.__LightModeColor('green', 0, 0.1)

    def __AlarmEffect(self):
        while True:
            self.__threadLock.acquire()
            if self.__alarmOn == False:
                self.__threadLock.release()
                self.__turnOff = False
                break
            self.__threadLock.release()
            self.__TurnAllOff()
            self.__LightOneColor('red', 255, 0.1)
            self.__LightModeColor('red', 1, 0.1)
            self.__LightOneColor('red', 0, 0.1)
            self.__LightModeColor('red', 0, 0.1)

    def __MainAnimation(self):
        if self.__mainAnimOn == False:
            self.__mainAnimOn = True
            self.__LightOneColor('green', 255, 0.1)
            self.__LightOneColor('blue', 255, 0.1)

    def RingTheAlarm(self):
        self.__threadLock.acquire()
        self.__alarmOn = True
        self.__threadLock.release()

    def StopTheAlarm(self):
        self.__threadLock.acquire()
        self.__alarmOn = False
        self.__threadLock.release()

    def TurnOnTheMode(self, modeColor):
        self.__LightModeColor(modeColor, 1, 0.1)

    def TurnOffTheMode(self, modeColor):
        self.__LightModeColor(modeColor, 0, 0.1)
