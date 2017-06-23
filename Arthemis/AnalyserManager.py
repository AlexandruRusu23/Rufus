"""
Analyser Manager module
"""

import time
import threading
import Queue
import VideoAnalyser
import DataAnalyser
import ResourceProvider

RESOURCE_PROVIDER = ResourceProvider.ResourceProvider()

class AnalyserManager(threading.Thread):
    """
    Analyser Manager class - responsible to manage the analysis for every
    type of data which is collected (sensors + camera)
    """
    def __init__(self):
        threading.Thread.__init__(self)

        self.__video_analyser = None
        self.__data_analyser = None

    def analyse_data(self, scanner_data_queue):
        """
        analyse the scanner data from an extern queue
        """
        current_thread = threading.currentThread()
        self.__data_analyser = DataAnalyser.DataAnalyser()
        __thread_timer = time.time()
        while getattr(current_thread, 'is_running', True):
            if time.time() - __thread_timer > 1000.0 / 1000.0:
                print 'hello'

    def analyse_video(self, mp4_files_queue):
        """
        analyse the mp4 files getting the name from an extern queue
        """
        current_thread = threading.currentThread()
        self.__video_analyser = VideoAnalyser.VideoAnalyser()
        __thread_timer = time.time()
        while getattr(current_thread, 'is_running', True):
            if time.time() - __thread_timer > 1000.0 / 1000.0:
                print 'hello2'
