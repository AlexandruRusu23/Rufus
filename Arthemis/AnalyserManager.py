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

    def analyse_data(self, scanner_data_queue, animations_cmd_queue):
        """
        analyse the scanner data from an extern queue
        """
        current_thread = threading.currentThread()
        self.__data_analyser = DataAnalyser.DataAnalyser()
        __thread_timer = time.time()
        while getattr(current_thread, 'is_running', True):
            if time.time() - __thread_timer > 100.0 / 1000.0:
                try:
                    scanner_data_dict = scanner_data_queue.get(False)
                except Queue.Empty:
                    continue
                self.__data_analyser.analyse(scanner_data_dict, animations_cmd_queue)
                notifications = self.__data_analyser.get_notifications()
                print notifications
                scanner_data_queue.task_done()

    def analyse_video(self, mp4_files_queue, analysed_mp4_files_queue):
        """
        analyse the mp4 files getting the name from an extern queue
        """
        current_thread = threading.currentThread()
        self.__video_analyser = VideoAnalyser.VideoAnalyser()
        __thread_timer = time.time()
        while getattr(current_thread, 'is_running', True):
            if time.time() - __thread_timer > 1000.0 / 1000.0:
                try:
                    file_name = mp4_files_queue.get(False)
                except Queue.Empty:
                    continue
                self.__video_analyser.face_recognition(file_name)
                self.__video_analyser.motion_detection(file_name)
                self.__video_analyser.human_recognition(file_name)
                self.__video_analyser.apply_detections(file_name)
                analysed_mp4_file_name = self.__video_analyser.get_analysed_file_name()
                analysed_mp4_files_queue.put(analysed_mp4_file_name, False)
                mp4_files_queue.task_done()

    def get_motion_status(self):
        """
        returns True if motion has been detected and False otherwise
        """
        if self.__data_analyser is not None:
            return self.__data_analyser.motion_status()
        else:
            return False
