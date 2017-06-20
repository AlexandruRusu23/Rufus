"""
camera record module
"""
import subprocess
import threading
import time
import DataProvider

RASPIVIDCMD = ["raspivid"]
TIMETOWAITFORABORT = 0.5

class CameraRecord(threading.Thread):
    """
    Camera recorder using raspivid
    """

    data_provider = DataProvider.DataProvider() #static

    def __init__(self, filePath, preview, timeout=10, other_options=None):
        threading.Thread.__init__(self)

        #setup the raspivid cmd
        self.__raspividcmd = RASPIVIDCMD

        #add file path, timeout and preview to options
        self.__raspividcmd.append("-o")
        self.__raspividcmd.append(filePath)
        self.__raspividcmd.append("-t")
        self.__raspividcmd.append(str(timeout))
        if bool(preview) is False:
            self.__raspividcmd.append("-n")

        #if there are other options, add them
        if other_options != None:
            self.__raspividcmd = self.__raspividcmd + other_options

        #set state to not running
        self.__is_running = False
        self.__running_lock = threading.Lock()

    def run(self):
        #run raspivid
        raspivid = subprocess.Popen(self.__raspividcmd)

        #loop until its set to stopped or it stops
        self.__is_running = True
        while raspivid.poll() is None:
            self.__running_lock.acquire()
            running_cond = self.__is_running
            self.__running_lock.release()

            if bool(running_cond) is False:
                break
            time.sleep(TIMETOWAITFORABORT)
        self.__is_running = False

        #kill raspivid if still running
        if bool(raspivid.poll()) is True:
            raspivid.kill()

    def stop_controller(self):
        """
        stop
        """
        self.__running_lock.acquire()
        self.__is_running = False
        self.__running_lock.release()
