import threading
import numpy as np
import time
import datetime
import cv2

class Surveillance(threading.Thread):

    def __init__(self, idCamera, frameWidth, frameHeight, fpsCamera):
        threading.Thread.__init__(self)
        self._isRunning = False
        self._camera = cv2.VideoCapture(idCamera)
        self._fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self._frameWidth = frameWidth
        self._frameHeight = frameHeight
        self._fpsCamera = fpsCamera
        self._fileOut = cv2.VideoWriter(self.__GetFileName(), self._fourcc, self._fpsCamera, (self._frameWidth, self._frameHeight))
        self._current_time = time.time()

    def __del__(self):
        'Terminated'

    def run(self):
        self._isRunning = True
        self._current_time = time.time()
        self.__Record()
        self._camera.release()
        self._fileOut.release()
        cv2.destroyAllWindows()

    def Stop(self):
        self._isRunning = False

    def __GetFileName(self):
        return 'VIDEO' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.avi'

    def __Record(self):
        while(self._camera.isOpened()):
            ret, frame = self._camera.read()
            if ret == True:
                if ((time.time() - self._current_time) > 10):
                    self._fileOut.release()
                    self._fileOut = cv2.VideoWriter(self.__GetFileName(), self._fourcc, self._fpsCamera, (self._frameWidth, self._frameHeight))
                    self._current_time = time.time()

                self._fileOut.write(frame)

                if (self._isRunning == False):
                    break
            else:
                self.Stop()
                break
