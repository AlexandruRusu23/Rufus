"""
Scanner Data Analyser module
"""
import time
import Queue
import UserCmdProvider
import ResourceProvider

RESOURCE_PROVIDER = ResourceProvider.ResourceProvider()

class DataAnalyser(object):
    """
    Scanner Data Analyser class - responsible to analyse the scanner data
    and return feedback, also commands for Animation Manager
    """
    def __init__(self):
        self.__user_cmd_provider = None
        self.__notifications_list = []
        self.__motion_status = False
        self.__temperature_threshold = None
        self.__humidity_threshold = None

    def analyse(self, scanner_data_dict, animations_cmd_queue):
        """
        Analyse the given dictionary
        """
        self.__update_user_preferences()
        try:
            scanner_data = scanner_data_dict.get(False)
        except Queue.Empty:
            return

        if len(scanner_data) > 1:
            # gas scenario
            value = scanner_data.get('gas')
            if len(value) > 0:
                gas_threshold = self.__user_cmd_provider.get_user_preference(
                    self.__user_cmd_provider.GAS_THRESHOLD
                )
                if gas_threshold is not None:
                    if value[0] > gas_threshold:
                        self.__notifications_list.append(
                            (RESOURCE_PROVIDER.NC_GAS_ALARM, str(value[1]))
                        )
                        try:
                            animations_cmd_queue.put(
                                RESOURCE_PROVIDER.AC_ACTIVATE_ALARM,
                                False
                            )
                        except Queue.Full:
                            pass
                    else:
                        try:
                            animations_cmd_queue.put(
                                RESOURCE_PROVIDER.AC_DEACTIVATE_ALARM,
                                False
                            )
                        except Queue.Full:
                            pass

            # temperature scenario
            value = scanner_data.get('temperature')
            if len(value) > 1:
                temp_threshold = self.__user_cmd_provider.get_user_preference(
                    self.__user_cmd_provider.TEMPERATURE_THRESHOLD
                )
                if temp_threshold is not None:
                    if value[0] > temp_threshold:
                        self.__notifications_list.append(
                            (RESOURCE_PROVIDER.NC_TEMPERATURE_HIGHER, str(value[1]))
                        )
                        try:
                            animations_cmd_queue.put(
                                RESOURCE_PROVIDER.AC_TEMPERATURE_WARNING_ON
                            )
                        except Queue.Full:
                            pass
                    else:
                        try:
                            animations_cmd_queue.put(
                                RESOURCE_PROVIDER.AC_TEMPERATURE_WARNING_OFF
                            )
                        except Queue.Full:
                            pass

            # humidity scenario
            value = scanner_data.get('humidity')
            if len(value) > 1:
                temp_threshold = self.__user_cmd_provider.get_user_preference(
                    self.__user_cmd_provider.HUMIDITY_THRESHOLD
                )
                if temp_threshold is not None:
                    if value[0] > temp_threshold:
                        self.__notifications_list.append(
                            (RESOURCE_PROVIDER.NC_HUMIDITY_HIGHER, str(value[1]))
                        )
                        try:
                            animations_cmd_queue.put(
                                RESOURCE_PROVIDER.AC_HUMIDITY_WARNING_ON
                            )
                        except Queue.Full:
                            pass
                    else:
                        try:
                            animations_cmd_queue.put(
                                RESOURCE_PROVIDER.AC_HUMIDITY_WARNING_OFF
                            )
                        except Queue.Full:
                            pass

            # motion scenario
            value = scanner_data.get('motion')
            if len(value) > 1:
                if value[0] > 0:
                    self.__notifications_list.append(
                        (RESOURCE_PROVIDER.NC_MOTION_DETECTED, str(value[1]))
                    )
                    try:
                        animations_cmd_queue.put(
                            RESOURCE_PROVIDER.AC_MOTION_ENABLED
                        )
                    except Queue.Full:
                        pass
                else:
                    try:
                        animations_cmd_queue.put(
                            RESOURCE_PROVIDER.AC_MOTION_DISABLED
                        )
                    except Queue.Full:
                        pass

        scanner_data_dict.task_done()

    def __update_user_preferences(self):
        self.__user_cmd_provider = UserCmdProvider.UserCmdProvider()
        self.__temperature_threshold = self.__user_cmd_provider.get_user_preference(
            self.__user_cmd_provider.TEMPERATURE_THRESHOLD
        )
        self.__humidity_threshold = self.__user_cmd_provider.get_user_preference(
            self.__user_cmd_provider.HUMIDITY_THRESHOLD
        )

    def motion_status(self):
        """
        returns True if motion has been detected and False otherwise
        """
        return self.__motion_status

    def get_notifications(self):
        """
        get the possible notifications
        """
        output = self.__notifications_list
        self.__notifications_list = []
        return output
