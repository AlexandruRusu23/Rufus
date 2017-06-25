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
        self.__notifications_list = []
        self.__motion_status = False
        self.__temperature_value = None
        self.__humidity_value = None
        self.__gas_value = None
        self.__user_cmd_provider = UserCmdProvider.UserCmdProvider()

    def analyse(self, scanner_data_dict, animations_cmd_queue):
        """
        Analyse the given dictionary
        """

        if scanner_data_dict is None:
            return

        if len(scanner_data_dict) > 0:
            # gas scenario
            value = scanner_data_dict.get('gas')
            if value is not None:
                if len(value) > 1:
                    self.__gas_value = int(value[0])
                    gas_threshold = self.__user_cmd_provider.get_user_preference(
                        self.__user_cmd_provider.GAS_THRESHOLD
                    )
                    if gas_threshold is not None:
                        if self.__gas_value > gas_threshold:
                            self.__notifications_list.append(
                                (RESOURCE_PROVIDER.NC_GAS_ALARM_ON, str(value[1]))
                            )
                        else:
                            self.__notifications_list.append(
                                (RESOURCE_PROVIDER.NC_GAS_ALARM_OFF, str(value[1]))
                            )

            # temperature scenario
            value = scanner_data_dict.get('temperature')
            if value is not None:
                if len(value) > 1:
                    self.__temperature_value = float(value[0])
                    temp_threshold = self.__user_cmd_provider.get_user_preference(
                        self.__user_cmd_provider.TEMPERATURE_THRESHOLD
                    )
                    if temp_threshold is not None:
                        if self.__temperature_value > temp_threshold:
                            self.__notifications_list.append(
                                (RESOURCE_PROVIDER.NC_TEMPERATURE_HIGHER, str(value[1]))
                            )
                        else:
                            self.__notifications_list.append(
                                (RESOURCE_PROVIDER.NC_TEMPERATURE_NORMAL, str(value[1]))
                            )

            # humidity scenario
            value = scanner_data_dict.get('humidity')
            if value is not None:
                if len(value) > 1:
                    self.__humidity_value = float(value[0])
                    temp_threshold = self.__user_cmd_provider.get_user_preference(
                        self.__user_cmd_provider.HUMIDITY_THRESHOLD
                    )
                    if temp_threshold is not None:
                        if self.__humidity_value > temp_threshold:
                            self.__notifications_list.append(
                                (RESOURCE_PROVIDER.NC_HUMIDITY_HIGHER, str(value[1]))
                            )
                        else:
                            self.__notifications_list.append(
                                (RESOURCE_PROVIDER.NC_HUMIDITY_NORMAL, str(value[1]))
                            )

            # motion scenario
            value = scanner_data_dict.get('motion')
            if value is not None:
                if len(value) > 1:
                    if int(value[0]) > 0:
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

    def update_animations(self, animations_cmd_queue):
        """
        verify constantly to make animations acording to user settings
        """
        threshold = self.__user_cmd_provider.get_user_preference(
            self.__user_cmd_provider.GAS_THRESHOLD
        )
        if threshold is not None and self.__gas_value is not None:
            if self.__gas_value > threshold:
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

        threshold = self.__user_cmd_provider.get_user_preference(
            self.__user_cmd_provider.TEMPERATURE_THRESHOLD
        )
        if threshold is not None and self.__temperature_value is not None:
            if float(self.__temperature_value) > threshold:
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

        threshold = self.__user_cmd_provider.get_user_preference(
            self.__user_cmd_provider.HUMIDITY_THRESHOLD
        )
        if threshold is not None and self.__humidity_value is not None:
            if float(self.__humidity_value) > threshold:
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
