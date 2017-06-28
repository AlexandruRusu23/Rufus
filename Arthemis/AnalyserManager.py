"""
Analyser Manager module
"""

import time
import threading
import Queue
import VideoAnalyser
import DataAnalyser
import ResourceProvider
import UserCmdProvider

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

        self.__data_analyse_thread = None
        self.__animations_update_thread = None

    def analyse_data(self, scanner_data_queue, animations_cmd_queue, notifications_queue):
        """
        analyse the scanner data from an extern queue
        """
        current_thread = threading.currentThread()
        self.__data_analyser = DataAnalyser.DataAnalyser()

        self.__data_analyse_thread = threading.Thread(
            target=self.__data_analyser.data_analyse,
            args=()
        )
        self.__data_analyse_thread.start()

        self.__animations_update_thread = threading.Thread(
            target=self.__data_analyser.update_animations,
            args=(animations_cmd_queue,)
        )
        self.__animations_update_thread.start()

        __thread_timer = time.time()
        while getattr(current_thread, 'is_running', True):
            if time.time() - __thread_timer > 100.0 / 1000.0:
                try:
                    scanner_data_dict = scanner_data_queue.get(False)
                except Queue.Empty:
                    continue
                self.__data_analyser.update_data(scanner_data_dict)
                try:
                    notifications_queue.put(self.__data_analyser.get_notifications(), False)
                except Queue.Full:
                    pass
                scanner_data_queue.task_done()
                __thread_timer = time.time()

        self.__data_analyse_thread.is_running = False
        self.__data_analyse_thread.join()
        print '[Analyser Manager] data_analyse_thread stopped'
        self.__animations_update_thread.is_running = False
        self.__animations_update_thread.join()
        print '[Analyser Manager] animations_update_thread stopped'

    def analyse_video(self, mp4_files_queue, analysed_mp4_files_queue):
        """
        analyse the mp4 files getting the name from an extern queue
        """
        current_thread = threading.currentThread()
        self.__video_analyser = VideoAnalyser.VideoAnalyser()
        __user_cmd_provider = UserCmdProvider.UserCmdProvider()
        __thread_timer = time.time()
        while getattr(current_thread, 'is_running', True):
            if time.time() - __thread_timer > 1000.0 / 1000.0:
                __thread_timer = time.time()
                try:
                    file_name = mp4_files_queue.get(False)
                except Queue.Empty:
                    continue

                # face detection
                condition = __user_cmd_provider.get_user_preference(
                    __user_cmd_provider.FACE_DETECTION_ENABLED
                )
                if condition is not None:
                    self.__video_analyser.enable_face_recognition(int(condition))

                # motion detection
                condition = __user_cmd_provider.get_user_preference(
                    __user_cmd_provider.MOTION_DETECTION_ENABLED
                )
                if condition is not None:
                    self.__video_analyser.enable_motion_detection(int(condition))

                # human detection
                condition = __user_cmd_provider.get_user_preference(
                    __user_cmd_provider.HUMAN_DETECTION_ENABLED
                )
                if condition is not None:
                    self.__video_analyser.enable_human_recognition(int(condition))

                self.__video_analyser.apply_detections(file_name)

                while getattr(current_thread, 'is_running', True):
                    try:
                        analysed_mp4_files_queue.put(file_name, False)
                    except Queue.Full:
                        continue
                    break
                mp4_files_queue.task_done()

    def get_motion_status(self):
        """
        returns True if motion has been detected and False otherwise
        """
        if self.__data_analyser is not None:
            return self.__data_analyser.motion_status()
        else:
            return False
