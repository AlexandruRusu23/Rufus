"""
App Manager module
"""

import threading
import time
import Queue
import VideoManager
import DataManager
import AnalyserManager
import AnimationManager
import ResourceProvider

RESOURCE_PROVIDER = ResourceProvider.ResourceProvider()

class ApplicationManager(threading.Thread):
    """
    App MGR class - responsible to manage intercommunications
    * maintain the stability and sinchronization between every thread
    """
    def __init__(self):
        threading.Thread.__init__(self)

        self.__scanner_data_queue = Queue.Queue(20)
        self.__mp4_files_queue = Queue.Queue(5)
        self.__analysed_mp4_files_queue = Queue.Queue(5)

        self.__is_running = False
        self.__is_running_lock = threading.Lock()

        self.__thread_timer = 0

        self.__data_manager = None
        self.__video_manager = None
        self.__analyser_manager = None
        self.__animation_manager = None

        self.__video_receive_thread = None # get file names from Video MGR
        self.__video_transfer_thread = None # send file names to Analyser MGR

        self.__data_receive_thread = None # get scanner data from Data MGR
        self.__data_transfer_thread = None # send scanner data to Analyser MGR

    def run(self):
        self.__data_manager = DataManager.DataManager()
        self.__video_manager = VideoManager.VideoManager()
        self.__analyser_manager = AnalyserManager.AnalyserManager()
        self.__animation_manager = AnimationManager.AnimationManager()

        self.__data_manager.start()
        self.__video_manager.start()
        #self.__analyser_manager.start()
        #self.__animation_manager.start()

        # scanner data receiver thread
        self.__data_receive_thread = threading.Thread(
            target=self.__data_manager.receive_scanner_data,
            args=(self.__scanner_data_queue,)
        )
        self.__data_receive_thread.start()

        # mp4 file names receiver thread
        self.__video_receive_thread = threading.Thread(
            target=self.__video_manager.receive_mp4_files,
            args=(self.__mp4_files_queue,)
        )
        self.__video_receive_thread.start()

        self.__is_running_lock.acquire()
        self.__is_running = True
        self.__is_running_lock.release()
        self.__thread_timer = time.time()
        while True:
            if time.time() - self.__thread_timer > 1000.0 / 1000.0:
                self.__is_running_lock.acquire()
                condition = self.__is_running
                self.__is_running_lock.release()
                if bool(condition) is False:
                    break
                self.__thread_timer = time.time()
