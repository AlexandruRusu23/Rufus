"""
Recorder module
"""
import subprocess
import threading
import time
import ResourceProvider

RESOURCE_PROVIDER = ResourceProvider.ResourceProvider() #static

RASPIVIDCMD = ["raspivid"]

class Recorder(threading.Thread):
    """
    Camera recorder using raspivid
    """
    def __init__(self, filePath, preview, timeout=10000, other_options=None):
        threading.Thread.__init__(self)

        #setup the raspivid cmd
        self.__raspividcmd = RASPIVIDCMD
        self.__raspividcmd.append("-w")
        self.__raspividcmd.append(str(
            RESOURCE_PROVIDER.get_string_table(
                RESOURCE_PROVIDER.CAMERA_RESOLUTION_WIDTH
            )
        ))
        self.__raspividcmd.append("-h")
        self.__raspividcmd.append(str(
            RESOURCE_PROVIDER.get_string_table(
                RESOURCE_PROVIDER.CAMERA_RESOLUTION_HEIGHT
            )
        ))

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

        self.__is_running = False
        self.__is_running_lock = threading.Lock()
        self.__thread_timer = 0

    def run(self):
        #run raspivid
        raspivid = subprocess.Popen(self.__raspividcmd)

        #loop until its set to stopped or it stops
        self.__is_running_lock.acquire()
        self.__is_running = True
        self.__is_running_lock.release()
        self.__thread_timer = time.time()
        while raspivid.poll() is None:
            if time.time() - self.__thread_timer > 300.0 / 1000.0:
                self.__is_running_lock.acquire()
                condition = self.__is_running
                self.__is_running_lock.release()
                if bool(condition) is False:
                    break
                self.__thread_timer = time.time()
        self.__is_running = False

        #kill raspivid if still running
        if bool(raspivid.poll()) is True:
            raspivid.kill()

    def stop(self):
        """
        stop the thread and stop recording the current file
        """
        self.__is_running_lock.acquire()
        self.__is_running = False
        self.__is_running_lock.release()
