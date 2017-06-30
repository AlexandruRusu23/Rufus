"""
Scanner Data Analyser module
"""
import time
import threading
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
        self.__notifications_list_lock = threading.Lock()

        self.__temperature_value = None
        self.__temperature_value_changed = None
        self.__temperature_value_lock = threading.Lock()

        self.__humidity_value = None
        self.__humidity_value_changed = None
        self.__humidity_value_lock = threading.Lock()

        self.__gas_value = None
        self.__gas_value_changed = None
        self.__gas_value_lock = threading.Lock()

        self.__motion_value = None
        self.__motion_value_changed = None
        self.__motion_value_lock = threading.Lock()

        self.__temperature_thresh = None
        self.__temperature_thresh_changed = None

        self.__humidity_thresh = None
        self.__humidity_thresh_changed = None

        self.__gas_thresh = None
        self.__gas_thresh_changed = None

        self.__user_cmd_provider = UserCmdProvider.UserCmdProvider()

        self.__animations_list = []
        self.__animations_list_lock = threading.Lock()

    def update_data(self, scanner_data_dict):
        """
        Update the data with the given dictionary
        """
        if scanner_data_dict is None:
            return

        print '[DataAnalyser]' + str(scanner_data_dict) + '\n'

        if len(scanner_data_dict) > 0:
            # gas
            value = scanner_data_dict.get('gas')
            if value is not None:
                if len(value) > 1:
                    self.__gas_value_lock.acquire()
                    self.__gas_value = value
                    self.__gas_value_changed = True
                    self.__gas_value_lock.release()

            # temperature
            value = scanner_data_dict.get('temperature')
            if value is not None:
                if len(value) > 1:
                    self.__temperature_value_lock.acquire()
                    self.__temperature_value = value
                    self.__temperature_value_changed = True
                    self.__temperature_value_lock.release()

            # humidity
            value = scanner_data_dict.get('humidity')
            if value is not None:
                if len(value) > 1:
                    self.__humidity_value_lock.acquire()
                    self.__humidity_value = value
                    self.__humidity_value_changed = True
                    self.__humidity_value_lock.release()

            # motion
            value = scanner_data_dict.get('motion')
            if value is not None:
                if len(value) > 1:
                    self.__motion_value_lock.acquire()
                    self.__motion_value = value
                    self.__motion_value_changed = True
                    self.__motion_value_lock.release()

    def data_analyse(self):
        """
        Analyse the data to decide if is needed a new notification or animation
        """
        current_thread = threading.currentThread()
        __thread_timer = time.time()
        while getattr(current_thread, 'is_running', True):
            if time.time() - __thread_timer > 200.0 / 1000.0:
                self.__refresh_data()
                # temperature
                if self.__temperature_value_changed is not None \
                and self.__temperature_thresh_changed is not None:
                    self.__temperature_value_lock.acquire()
                    if bool(self.__temperature_value_changed) is True \
                    or bool(self.__temperature_thresh_changed) is True:
                        if float(self.__temperature_value[0]) > self.__temperature_thresh:
                            self.__append_animation(
                                RESOURCE_PROVIDER.AC_TEMPERATURE_WARNING_ON
                            )
                            self.__append_notification(
                                RESOURCE_PROVIDER.NC_TEMPERATURE_HIGHER,
                                self.__temperature_value[1]
                            )
                        else:
                            self.__append_animation(
                                RESOURCE_PROVIDER.AC_TEMPERATURE_WARNING_OFF
                            )
                            self.__append_notification(
                                RESOURCE_PROVIDER.NC_TEMPERATURE_NORMAL,
                                self.__temperature_value[1]
                            )
                        self.__temperature_thresh_changed = False
                        self.__temperature_value_changed = False
                    self.__temperature_value_lock.release()

                # humidity
                if self.__humidity_value_changed is not None \
                and self.__humidity_thresh_changed is not None:
                    self.__humidity_value_lock.acquire()
                    if bool(self.__humidity_value_changed) is True \
                    or bool(self.__humidity_thresh_changed) is True:
                        if float(self.__humidity_value[0]) > self.__humidity_thresh:
                            self.__append_animation(
                                RESOURCE_PROVIDER.AC_HUMIDITY_WARNING_ON
                            )
                            self.__append_notification(
                                RESOURCE_PROVIDER.NC_HUMIDITY_HIGHER,
                                self.__humidity_value[1]
                            )
                        else:
                            self.__append_animation(
                                RESOURCE_PROVIDER.AC_HUMIDITY_WARNING_OFF
                            )
                            self.__append_notification(
                                RESOURCE_PROVIDER.NC_HUMIDITY_NORMAL,
                                self.__humidity_value[1]
                            )
                        self.__humidity_thresh_changed = False
                        self.__humidity_value_changed = False
                    self.__humidity_value_lock.release()

                # gas
                if self.__gas_value_changed is not None \
                and self.__gas_thresh_changed is not None:
                    self.__gas_value_lock.acquire()
                    if bool(self.__gas_value_changed) is True \
                    or bool(self.__gas_thresh_changed) is True:
                        if int(self.__gas_value[0]) > self.__gas_thresh:
                            self.__append_animation(
                                RESOURCE_PROVIDER.AC_ACTIVATE_ALARM
                            )
                            self.__append_notification(
                                RESOURCE_PROVIDER.NC_GAS_ALARM_ON,
                                self.__gas_value[1]
                            )
                        else:
                            self.__append_animation(
                                RESOURCE_PROVIDER.AC_DEACTIVATE_ALARM
                            )
                            self.__append_notification(
                                RESOURCE_PROVIDER.NC_GAS_ALARM_OFF,
                                self.__gas_value[1]
                            )
                        self.__gas_thresh_changed = False
                        self.__gas_value_changed = False
                    self.__gas_value_lock.release()

                # motion
                self.__motion_value_lock.acquire()
                if bool(self.__motion_value_changed) is True:
                    if int(self.__motion_value[0]) > 0:
                        self.__append_animation(
                            RESOURCE_PROVIDER.AC_MOTION_ENABLED
                        )
                        self.__append_notification(
                            RESOURCE_PROVIDER.NC_MOTION_DETECTED,
                            self.__motion_value[1]
                        )
                    else:
                        self.__append_animation(
                            RESOURCE_PROVIDER.AC_MOTION_DISABLED
                        )
                    self.__motion_value_changed = False
                self.__motion_value_lock.release()

                __thread_timer = time.time()

    def __refresh_data(self):
        gas_threshold = self.__user_cmd_provider.get_user_preference(
            self.__user_cmd_provider.GAS_THRESHOLD
        )
        if gas_threshold is not None:
            if gas_threshold != self.__gas_thresh:
                self.__gas_thresh_changed = True
                self.__gas_thresh = int(gas_threshold)

        humi_threshold = self.__user_cmd_provider.get_user_preference(
            self.__user_cmd_provider.HUMIDITY_THRESHOLD
        )
        if humi_threshold is not None:
            if humi_threshold != self.__humidity_thresh:
                self.__humidity_thresh_changed = True
                self.__humidity_thresh = int(humi_threshold)


        temp_threshold = self.__user_cmd_provider.get_user_preference(
            self.__user_cmd_provider.TEMPERATURE_THRESHOLD
        )
        if temp_threshold is not None:
            if temp_threshold != self.__temperature_thresh:
                self.__temperature_thresh_changed = True
                self.__temperature_thresh = int(temp_threshold)

    def update_animations(self, animations_cmd_queue):
        """
        send the animations to an extern queue
        """
        current_thread = threading.currentThread()
        __thread_timer = time.time()
        while getattr(current_thread, 'is_running', True):
            if time.time() - __thread_timer > 200.0 / 1000.0:
                self.__animations_list_lock.acquire()
                animations_list = self.__animations_list
                self.__animations_list = []
                self.__animations_list_lock.release()
                for elem in animations_list:
                    while getattr(current_thread, 'is_running', True):
                        try:
                            animations_cmd_queue.put(elem, False)
                        except Queue.Full:
                            continue
                        break
                __thread_timer = time.time()

    def __append_animation(self, animation_type):
        self.__animations_list_lock.acquire()
        self.__animations_list.append(animation_type)
        self.__animations_list_lock.release()

    def __append_notification(self, notification_type, time_collected):
        self.__notifications_list_lock.acquire()
        self.__notifications_list.append(
            (notification_type, time_collected)
        )
        self.__notifications_list_lock.release()

    def get_notifications(self):
        """
        get the possible notifications
        """
        self.__notifications_list_lock.acquire()
        output = self.__notifications_list
        self.__notifications_list = []
        self.__notifications_list_lock.release()
        return output
