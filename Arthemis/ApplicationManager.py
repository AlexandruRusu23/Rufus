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
import DatabaseManager
import ResourceProvider
import UserCmdProvider

RESOURCE_PROVIDER = ResourceProvider.ResourceProvider()

class ApplicationManager(threading.Thread):
    """
    App MGR class - responsible to manage intercommunications
    * maintain the stability and sinchronization between every thread
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.__user_cmd_provider = None

        self.__scanner_data_queue = Queue.Queue(20)
        self.__mp4_files_queue = Queue.Queue(20)
        self.__analysed_mp4_files_queue = Queue.Queue(20)
        self.__animations_queue = Queue.Queue(20)
        self.__notifications_queue = Queue.Queue(20)

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

        self.__notifications_thread = None # upload notifications

        self.__animations_thread = None # execute animations

    def run(self):
        self.__user_cmd_provider = UserCmdProvider.UserCmdProvider()

        self.__data_manager = DataManager.DataManager()
        self.__video_manager = VideoManager.VideoManager()
        self.__analyser_manager = AnalyserManager.AnalyserManager()
        self.__animation_manager = AnimationManager.AnimationManager()

        self.__data_manager.start()
        self.__video_manager.start()

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

        # transfer scanner data to be analysed
        self.__data_transfer_thread = threading.Thread(
            target=self.__analyser_manager.analyse_data,
            args=(self.__scanner_data_queue, self.__animations_queue, self.__notifications_queue,)
        )
        self.__data_transfer_thread.start()

        # transfer mp4 file names to be analysed
        self.__video_transfer_thread = threading.Thread(
            target=self.__analyser_manager.analyse_video,
            args=(self.__mp4_files_queue, self.__analysed_mp4_files_queue,)
        )
        self.__video_transfer_thread.start()

        # notifications upload thread
        self.__notifications_thread = threading.Thread(
            target=self.upload_notifications,
            args=(self.__notifications_queue,)
        )
        self.__notifications_thread.start()

        # execute animations thread
        self.__animations_thread = threading.Thread(
            target=self.__animation_manager.animates,
            args=(self.__animations_queue,)
        )
        self.__animations_thread.start()

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

                video_condition = self.__user_cmd_provider.get_user_preference(
                    self.__user_cmd_provider.VIDEO_ENABLED
                )
                if video_condition is not None:
                    if int(video_condition) == 0:
                        self.__video_manager.enable_recording(False)
                    else:
                        if bool(self.__analyser_manager.get_motion_status()) is False:
                            self.__video_manager.enable_recording(False)
                        else:
                            self.__video_manager.enable_recording(True)

        # wait for every thread to finish their work
        self.__data_manager.stop()
        self.__data_manager.join()
        self.__video_manager.stop()
        self.__video_manager.join()
        self.__data_receive_thread.is_running = False
        self.__data_receive_thread.join()
        self.__video_receive_thread.is_running = False
        self.__video_receive_thread.join()
        self.__data_transfer_thread.is_running = False
        self.__data_transfer_thread.join()
        self.__video_transfer_thread.is_running = False
        self.__video_transfer_thread.join()
        self.__notifications_thread.is_running = False
        self.__notifications_thread.join()
        self.__animations_thread.is_running = False
        self.__animations_thread.join()

    def stop(self):
        """
        stop the entire application
        """
        self.__is_running_lock.acquire()
        self.__is_running = False
        self.__is_running_lock.release()

    def upload_notifications(self, notifications_queue):
        """
        Upload the notifications via DB MGR
        """
        current_thread = threading.currentThread()
        __database_manager = DatabaseManager.DatabaseManager()
        __thread_timer = time.time()
        while getattr(current_thread, 'is_running', True):
            if time.time() - __thread_timer > 200.0 / 1000.0:
                __thread_timer = time.time()
                try:
                    notifications = notifications_queue.get(False)
                except Queue.Empty:
                    continue
                for elem in notifications:
                    __database_manager.insert_data_in_database(elem, 'HOME_SCANNER_NOTIFICATIONS')
                notifications_queue.task_done()
