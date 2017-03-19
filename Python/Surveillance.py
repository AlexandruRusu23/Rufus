import threading
import numpy as np
import time
import datetime
import cv2

class Surveillance(threading.Thread):
    #static field to increment the id of the camera to prevent the cases there's more than one camera
    idCamera = 0

    def __init__(self, frameWidth, frameHeight, fpsCamera):
        threading.Thread.__init__(self)
        self._runningLock = threading.Lock()
        self._isRunning = False
        self._camera = cv2.VideoCapture(Surveillance.idCamera)
        Surveillance.idCamera = Surveillance.idCamera + 1
        self._fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self._frameWidth = frameWidth
        self._frameHeight = frameHeight
        self._fpsCamera = fpsCamera
        self._fileOut = cv2.VideoWriter(self.__GetFileName(), self._fourcc, self._fpsCamera, (self._frameWidth, self._frameHeight))
        self._current_time = time.time()

    def run(self):
        self._isRunning = True
        self._current_time = time.time()
        self.__Record()
        self._camera.release()
        self._fileOut.release()
        cv2.destroyAllWindows()

    def __Record(self):
        while(self._camera.isOpened()):
            ret, frame = self._camera.read()
            if ret == True:
                if ((time.time() - self._current_time) > 10):
                    self._fileOut.release()
                    self._fileOut = cv2.VideoWriter(self.__GetFileName(), self._fourcc, self._fpsCamera, (self._frameWidth, self._frameHeight))
                    self._current_time = time.time()

                self._fileOut.write(frame)

                self._runningLock.acquire()
                if (self._isRunning == False):
                    self._runningLock.release()
                    break
                self._runningLock.release()

            else:
                self.Stop()
                break

    def Stop(self):
        self._runningLock.acquire()
        self._isRunning = False
        self._runningLock.release()

    def __GetFileName(self):
        return 'VIDEO' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.avi'
