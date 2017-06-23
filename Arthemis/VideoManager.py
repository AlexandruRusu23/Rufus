"""
store video module
"""
import os
import subprocess
import threading
import time
import datetime
import Queue
import Recorder
import ResourceProvider

MP4BOX = "MP4Box"
RESOURCE_PROVIDER = ResourceProvider.ResourceProvider()

class VideoManager(threading.Thread):
    """
    store
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.__recorder_thread = None
        self.__video_camera = None

        self.__is_running = False
        self.__is_running_lock = threading.Lock()

        self.__record_video_enabled = False
        self.__record_video_enabled_lock = threading.Lock()

        self.__convert_thread = None

        self.__raw_files_queue = Queue.Queue(5)
        self.__converted_files_queue = Queue.Queue(5)

        self.__thread_timer = 0

    def run(self):
        """
        run
        """
        self.__is_running_lock.acquire()
        self.__is_running = True
        self.__is_running_lock.release()

        self.__recorder_thread = \
            threading.Thread(target=self.__record_video, args=())
        self.__recorder_thread.start()

        self.__convert_thread = \
            threading.Thread(target=self.__convert_to_mp4, args=())
        self.__convert_thread.start()

        self.__thread_timer = time.time()

        while True:
            if time.time() - self.__thread_timer > 1000.0 / 1000.0:
                self.__is_running_lock.acquire()
                condition = self.__is_running
                self.__is_running_lock.release()

                if bool(condition) is False:
                    break
                self.__thread_timer = time.time()

        self.__recorder_thread.is_running = False
        self.__recorder_thread.join()
        self.__convert_thread.is_running = False
        self.__convert_thread.join()

    def stop(self):
        """
        stop
        """
        self.__is_running_lock.acquire()
        self.__is_running = False
        self.__is_running_lock.release()

    def enable_recording(self, enabled):
        """
        enable or disable recording giving a boolean as argument
        """
        self.__record_video_enabled_lock.acquire()
        self.__record_video_enabled = enabled
        self.__record_video_enabled_lock.release()

    def __record_video(self):
        current_thread = threading.currentThread()

        frames_per_second = \
                    RESOURCE_PROVIDER.get_string_table(RESOURCE_PROVIDER.CAMERA_FRAMERATE)
        duration = RESOURCE_PROVIDER.get_string_table(RESOURCE_PROVIDER.CAMERA_DURATION)

        while getattr(current_thread, 'is_running', True):

            self.__record_video_enabled_lock.acquire()
            condition = self.__record_video_enabled
            self.__record_video_enabled_lock.release()

            if bool(condition) is True:
                file_name = self.__get_file_name()
                self.__video_camera = Recorder.Recorder(\
                    file_name, False, str(duration), ["-fps", str(frames_per_second)])
                self.__video_camera.start()
                self.__thread_timer = time.time()
                while self.__video_camera.isAlive():
                    if time.time() - self.__thread_timer > 300.0 / 1000.0:
                        if getattr(current_thread, 'is_running', False):
                            break
                        self.__thread_timer = time.time()

                self.__video_camera.stop()
                self.__video_camera.join()

                while getattr(current_thread, 'is_running', True):
                    try:
                        self.__raw_files_queue.put(file_name, False)
                    except Queue.Full:
                        time.sleep(0.1)
                        continue
                    break

    def __get_file_name(self):
        return 'VIDEO' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.h264'

    def __convert_to_mp4(self):
        current_thread = threading.currentThread()
        while getattr(current_thread, 'is_running', True):
            try:
                file_name = self.__raw_files_queue.get(False)
            except Queue.Empty:
                time.sleep(0.5)
                continue

            converted_file_name = os.path.splitext(file_name)[0] + '.mp4'
            convert_command = []
            convert_command.append(MP4BOX)
            convert_command.append("-add")
            convert_command.append(file_name)
            convert_command.append(converted_file_name)

            convert_process = subprocess.Popen(convert_command)

            while convert_process.poll() is None:
                time.sleep(0.1)

            while getattr(current_thread, 'is_running', True):
                try:
                    self.__converted_files_queue.put(converted_file_name, False)
                except Queue.Full:
                    time.sleep(0.1)
                    continue
                break

            clear_command = []
            clear_command.append('rm')
            clear_command.append(file_name)

            clear_process = subprocess.Popen(clear_command)

            while clear_process.poll() is None:
                time.sleep(0.1)

            self.__raw_files_queue.task_done()

    def __get_mp4_file_name(self):
        """
        get mp4 file name from queue
        """
        try:
            output = self.__converted_files_queue.get(False)
        except Queue.Empty:
            return ''

        self.__converted_files_queue.task_done()
        return output

    def receive_mp4_files(self, mp4_files_queue):
        """
        populate an extern queue with the name of the mp4 files
        """
        current_thread = threading.currentThread()
        __thread_timer = time.time()
        while getattr(current_thread, 'is_running', True):
            if time.time() - __thread_timer > 1000.0 / 1000.0:
                output = self.__get_mp4_file_name()
                if len(output) > 0:
                    while getattr(current_thread, 'is_running', True):
                        try:
                            mp4_files_queue.put(output, False)
                        except Queue.Full:
                            time.sleep(0.1)
                            continue
                        break
                __thread_timer = time.time()
