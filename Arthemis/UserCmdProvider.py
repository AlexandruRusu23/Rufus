"""
User Commands Provider module
"""

import DatabaseManager
import ResourceProvider

RESOURCE_PROVIDER = ResourceProvider.ResourceProvider()

class UserCmdProvider(object):
    """
    User commands provider class
    """

    TEMPERATURE_THRESHOLD = 'temp_thresh'
    HUMIDITY_THRESHOLD = 'humidity_thresh'
    GAS_THRESHOLD = 'gas_threshold'
    VIDEO_ENABLED = 'video_enabled'
    FACE_DETECTION_ENABLED = 'face_enabled'
    MOTION_DETECTION_ENABLED = 'motion_enabled'
    HUMAN_DETECTION_ENABLED = 'human_enabled'

    def __init__(self):
        self.__database_manager = None

        self.__temperature_threshold = None
        self.__humidity_threshold = None
        self.__gas_threshold = None
        self.__video_enabled = None
        self.__face_detection_enabled = None
        self.__motion_detection_enabled = None
        self.__human_detection_enabled = None

        self.__db_connected = False

    def __collect_data(self):
        """
        get data from MySQLdb server
        """
        if bool(self.__db_connected) is False:
            self.__database_manager = DatabaseManager.DatabaseManager()
            self.__db_connected = True

        user_settings = \
            self.__database_manager.get_data_from_database('HOME_SCANNER_USER_SETTINGS')
        if len(user_settings) > 7:
            for elem in user_settings:
                self.__temperature_threshold = int(elem[1])
                self.__humidity_threshold = int(elem[2])
                self.__gas_threshold = int(elem[3])
                self.__video_enabled = int(elem[4])
                self.__face_detection_enabled = int(elem[5])
                self.__motion_detection_enabled = int(elem[6])
                self.__human_detection_enabled = int(elem[7])

    def get_user_preference(self, preference_type):
        """
        Get the user preference for every type of settings
        """
        self.__collect_data()
        if preference_type == UserCmdProvider.TEMPERATURE_THRESHOLD:
            return self.__temperature_threshold
        elif preference_type == UserCmdProvider.HUMAN_DETECTION_ENABLED:
            return self.__humidity_threshold
        elif preference_type == UserCmdProvider.GAS_THRESHOLD:
            return self.__gas_threshold
        elif preference_type == UserCmdProvider.VIDEO_ENABLED:
            return self.__video_enabled
        elif preference_type == UserCmdProvider.FACE_DETECTION_ENABLED:
            return self.__face_detection_enabled
        elif preference_type == UserCmdProvider.MOTION_DETECTION_ENABLED:
            return self.__motion_detection_enabled
        elif preference_type == UserCmdProvider.HUMAN_DETECTION_ENABLED:
            return self.__human_detection_enabled
