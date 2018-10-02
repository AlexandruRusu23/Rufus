"""
Analyser Manager module
"""

import subprocess
import time
import threading
import Queue
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
                __thread_timer = time.time()
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
        __user_cmd_provider = UserCmdProvider.UserCmdProvider()
        __thread_timer = time.time()
        while getattr(current_thread, 'is_running', True):
            if time.time() - __thread_timer > 1000.0 / 1000.0:
                __thread_timer = time.time()
                try:
                    file_name = mp4_files_queue.get(False)
                except Queue.Empty:
                    continue

                video_analyse_cmd = ["python"]
                video_analyse_cmd.append("VideoAnalyser.py")
                video_analyse_cmd.append("--file")
                video_analyse_cmd.append(str(file_name))

                # face detection
                condition = __user_cmd_provider.get_user_preference(
                    __user_cmd_provider.FACE_DETECTION_ENABLED
                )
                if condition is not None:
                    video_analyse_cmd.append("--face")
                    video_analyse_cmd.append(str(condition))

                # motion detection
                condition = __user_cmd_provider.get_user_preference(
                    __user_cmd_provider.MOTION_DETECTION_ENABLED
                )
                if condition is not None:
                    video_analyse_cmd.append("--motion")
                    video_analyse_cmd.append(str(condition))

                # human detection
                condition = __user_cmd_provider.get_user_preference(
                    __user_cmd_provider.HUMAN_DETECTION_ENABLED
                )
                if condition is not None:
                    video_analyse_cmd.append("--human")
                    video_analyse_cmd.append(str(condition))

                analyse_video_process = subprocess.Popen(video_analyse_cmd)

                while analyse_video_process.poll() is None:
                    if getattr(current_thread, 'is_running', False):
                        break
                    time.sleep(0.1)

                if bool(analyse_video_process.poll()) is True:
                    analyse_video_process.kill()

                while getattr(current_thread, 'is_running', True):
                    try:
                        analysed_mp4_files_queue.put(file_name, False)
                    except Queue.Full:
                        continue
                    break
                mp4_files_queue.task_done()

