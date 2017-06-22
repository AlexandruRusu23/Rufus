"""
User Commands Manager module
"""

import threading
import time
import DatabaseManager
import ResourceProvider

RESOURCE_PROVIDER = ResourceProvider.ResourceProvider()

class UserCmdManager(threading.Thread):
    """
    User commands manager class
    """

    TEMPERATURE_THRESHOLD = 'temp_thresh'
    HUMIDITY_THRESHOLD = 'humidity_thresh'
    FACE_DETECTION_ENABLED = 'face_enabled'
    MOTION_DETECTION_ENABLED = 'motion_enabled'
    HUMAN_DETECTION_ENABLED = 'human_enabled'

    def __init__(self):
        threading.Thread.__init__(self)
        self.__database_name = RESOURCE_PROVIDER.get_string_table(RESOURCE_PROVIDER.DATABASE_NAME)
        self.__database_manager = None

        self.__is_running = False
        self.__is_running_lock = threading.Lock()

        self.__thread_timer = 0
        self.__provider_timer = 0

        self.__temperature_threshold = None
        self.__humidity_threshold = None
        self.__face_detection_enabled = None
        self.__motion_detection_enabled = None
        self.__human_detection_enabled = None

    def run(self):
        self.__database_manager = DatabaseManager.DatabaseManager(self.__database_name)
        self.__is_running_lock.acquire()
        self.__is_running = True
        self.__is_running_lock.release()
        while True:
            if time.time() - self.__thread_timer > 1000.0 / 1000.0:
                self.__is_running_lock.acquire()
                condition = self.__is_running
                self.__is_running_lock.release()
                if bool(condition) is False:
                    break
                self.__thread_timer = time.time()

            if time.time() - self.__provider_timer > 1000.0 / 1000.0:
                self.__analyse_user_settings()
                self.__provider_timer = time.time()

    def __analyse_user_settings(self):
        """
        analyse user preferrences from DB
        """
        user_settings = \
            self.__database_manager.get_data_from_database('HOME_SCANNER_USER_SETTINGS')
        if len(user_settings) > 5:
            for elem in user_settings:
                self.__temperature_threshold = int(elem[1])
                self.__humidity_threshold = int(elem[2])
                self.__face_detection_enabled = int(elem[3])
                self.__motion_detection_enabled = int(elem[4])
                self.__human_detection_enabled = int(elem[5])

    def get_user_preference(self, preference_type):
        """
        Get the user preference for every type of settings
        """
        if preference_type == UserCmdManager.TEMPERATURE_THRESHOLD:
            return self.__temperature_threshold
        elif preference_type == UserCmdManager.HUMAN_DETECTION_ENABLED:
            return self.__humidity_threshold
        elif preference_type == UserCmdManager.FACE_DETECTION_ENABLED:
            return self.__face_detection_enabled
        elif preference_type == UserCmdManager.MOTION_DETECTION_ENABLED:
            return self.__motion_detection_enabled
        elif preference_type == UserCmdManager.HUMAN_DETECTION_ENABLED:
            return self.__human_detection_enabled
