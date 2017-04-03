"""
store video module
"""
import os
import subprocess
import threading
import time
import datetime
import CameraRecord
import DataProvider

MP4BOX = ["MP4Box"]

class StoreVideo(threading.Thread):
    """
    store
    """

    data_provider = DataProvider.DataProvider() #static

    def __init__(self):
        threading.Thread.__init__(self)
        self.__video_camera = None
        self.__is_running = True
        self.__running_lock = threading.Lock()

    def run(self):
        """
        run
        """
        try:
            while True:
                self.__running_lock.acquire()
                running_cond = self.__is_running
                self.__running_lock.release()

                if bool(running_cond) is False:
                    break

                file_name = self.__get_file_name()
                frames_per_second = StoreVideo.data_provider.get_string_table('CAMERA_FRAMERATE')
                duration = int(StoreVideo.data_provider.get_string_table('CAMERA_DURATION'))
                self.__video_camera = CameraRecord.CameraRecord(\
                    file_name, duration, False, ["-fps", frames_per_second])
                self.__video_camera.start()
                while self.__video_camera.isAlive():
                    self.__running_lock.acquire()
                    running_cond = self.__is_running
                    self.__running_lock.release()

                    if bool(running_cond) is False:
                        break
                    time.sleep(0.5)

                self.__convert_to_mp4(file_name)

        #Ctrl C
        except KeyboardInterrupt:
            print "Cancelled"

        #Error
        except:
            print "Unexpected error:"
            raise

        finally:
            print "Stopping raspivid controller"
            self.__video_camera.stop_controller()
            self.__video_camera.join()

    def stop(self):
        """
        stop
        """
        self.__running_lock.acquire()
        self.__is_running = False
        self.__running_lock.release()

    def __get_file_name(self):
        return 'VIDEO' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.h264'

    def __convert_to_mp4(self, file_name):
        converted_file_name = os.path.splitext(file_name)[0] + '.mp4'
        convert_command = MP4BOX
        convert_command.append("-all")
        convert_command.append(file_name)
        convert_command.append(converted_file_name)

        convert_process = subprocess.Popen(convert_command)

        while convert_process.poll() is None:
            time.sleep(0.5)

        if bool(convert_process.poll()) is True:
            convert_process.kill()
