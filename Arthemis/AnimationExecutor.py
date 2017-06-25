"""
Animation Executor module
"""

import threading
import time
import random
import Queue
import SerialManager
import ResourceProvider

RESOURCE_PROVIDER = ResourceProvider.ResourceProvider()

class AnimationExecutor(threading.Thread):
    """
    Animation Executor class
    - it's job is to execute the commands received from Animation Manager
    """
    _ON = 1
    _OFF = 0
    _RED_COLOR = RESOURCE_PROVIDER.get_string_table('RED_COLOR_PIN')
    _GREEN_COLOR = RESOURCE_PROVIDER.get_string_table('GREEN_COLOR_PIN')
    _BLUE_COLOR = RESOURCE_PROVIDER.get_string_table('BLUE_COLOR_PIN')
    _BLUE_MODE = RESOURCE_PROVIDER.get_string_table('BLUE_MODE_PIN')
    _RED_MODE = RESOURCE_PROVIDER.get_string_table('RED_MODE_PIN')
    _YELLOW_MODE = RESOURCE_PROVIDER.get_string_table('YELLOW_MODE_PIN')
    _GREEN_MODE = RESOURCE_PROVIDER.get_string_table('GREEN_MODE_PIN')

    def __init__(self):
        threading.Thread.__init__(self)

        self.__animations_queue = Queue.PriorityQueue(20)

        self.__is_running = False
        self.__is_running_lock = threading.Lock()

        self.__alarm_enabled = False
        self.__alarm_enabled_lock = threading.Lock()
        self.__alarm_thread = None

        self.__warning_type = None
        self.__warning_type_lock = threading.Lock()

        self.__thread_timer = 0
        self.__animation_timer = 0

        self.__serial_manager = None
        self.__serial_lock = threading.Lock()

    def __connect_to_board(self):
        board_ratio = RESOURCE_PROVIDER.get_string_table('ANIMATOR_BOARD_RATIO')
        board_name = RESOURCE_PROVIDER.get_board_name(
            RESOURCE_PROVIDER.get_string_table('ANIMATOR_BOARD')
        )
        if board_name and board_ratio:
            self.__serial_manager = SerialManager.SerialManager(board_name, int(board_ratio))
            self.__serial_manager.connect_to_board()
            return True
        else:
            return False

    def run(self):
        if bool(self.__connect_to_board()) is False:
            print 'Stopped'
            return

        self.__is_running_lock.acquire()
        self.__is_running = True
        self.__is_running_lock.release()

        # alarm watcher thread
        self.__alarm_thread = threading.Thread(
            target=self.__alarm_animation,
            args=()
        )
        self.__alarm_thread.start()

        self.__thread_timer = time.time()

        while True:
            if time.time() - self.__thread_timer > 1000.0 / 1000.0:
                self.__is_running_lock.acquire()
                condition = self.__is_running
                self.__is_running_lock.release()

                if bool(condition) is False:
                    break

                # main animation
                self.__main_animation()

                self.__thread_timer = time.time()

            if time.time() - self.__animation_timer > 100.0 / 1000.0:
                try:
                    animation = self.__animations_queue.get(False)
                except Queue.Empty:
                    continue
                if len(animation) > 1:
                    if animation[0] == 1: # alarm type
                        self.__update_alarm_status(animation[1])
                    else: # warning type
                        self.__update_warning_animation(animation[1])
                self.__animation_timer = time.time()

        self.__alarm_thread.is_running = False
        self.__alarm_thread.join()
        self.__turn_all_off()

    def stop(self):
        """
        stop the main thread
        """
        self.__is_running_lock.acquire()
        self.__is_running = False
        self.__is_running_lock.release()

    def execute(self, animation_command):
        """
        execute the given animation command
        """
        if animation_command == RESOURCE_PROVIDER.AC_ACTIVATE_ALARM or \
            animation_command == RESOURCE_PROVIDER.AC_DEACTIVATE_ALARM:
            try:
                self.__animations_queue.put((1, animation_command), False)
            except Queue.Full:
                return False
        else:
            try:
                self.__animations_queue.put((2, animation_command), False)
            except Queue.Full:
                return False
        return True

    def __turn_all_off(self):
        self.__light_one_rgb_color(AnimationExecutor._RED_COLOR, 0)
        self.__light_one_rgb_color(AnimationExecutor._GREEN_COLOR, 0)
        self.__light_one_rgb_color(AnimationExecutor._BLUE_COLOR, 0)
        self.__light_mode_color(AnimationExecutor._BLUE_MODE, AnimationExecutor._OFF)
        self.__light_mode_color(AnimationExecutor._RED_MODE, AnimationExecutor._OFF)
        self.__light_mode_color(AnimationExecutor._YELLOW_MODE, AnimationExecutor._OFF)
        self.__light_mode_color(AnimationExecutor._GREEN_MODE, AnimationExecutor._OFF)

    def __light_one_rgb_color(self, color_type, intensity):
        command = RESOURCE_PROVIDER.get_string_table('ANALOG_WRITE')
        command = command + str(color_type) + '/' + str(intensity)+ '/'
        self.__do_animation(command)

    def __light_mode_color(self, color_type, status):
        command = RESOURCE_PROVIDER.get_string_table('DIGITAL_WRITE')
        command = command + str(color_type) + '/' + str(status)+ '/'
        self.__do_animation(command)

    def __turn_on_the_mode(self, mode_color):
        """
        turn on the led for a specific mode
        """
        self.__light_mode_color(mode_color, AnimationExecutor._ON)

    def __turn_off_the_mode(self, mode_color):
        """
        turn off the led for a specific mode
        """
        self.__light_mode_color(mode_color, AnimationExecutor._OFF)

    def __update_alarm_status(self, alarm_status):
        if alarm_status == RESOURCE_PROVIDER.AC_ACTIVATE_ALARM:
            self.__alarm_enabled_lock.acquire()
            self.__alarm_enabled = True
            self.__alarm_enabled_lock.release()
        elif alarm_status == RESOURCE_PROVIDER.AC_DEACTIVATE_ALARM:
            self.__alarm_enabled_lock.acquire()
            self.__alarm_enabled = False
            self.__alarm_enabled_lock.release()

    def __update_warning_animation(self, warning_type):
        self.__warning_type_lock.acquire()
        self.__warning_type = warning_type
        self.__warning_type_lock.release()

    def __do_animation(self, commands_list):
        """
        send the commands list given as argument to serial manager
        """
        if commands_list:
            commands_list = [commands_list]
            self.__serial_lock.acquire()
            self.__serial_manager.set_scanner_commands(commands_list)
            self.__serial_manager.execute_commands()
            self.__serial_lock.release()

    def __alarm_animation(self):
        current_thread = threading.currentThread()
        __thread_timer = time.time()
        while getattr(current_thread, 'is_running', True):
            if time.time() - __thread_timer > 200.0 / 1000.0:
                __thread_timer = time.time()
                self.__alarm_enabled_lock.acquire()
                alarm_cond = self.__alarm_enabled
                self.__alarm_enabled_lock.release()

                if bool(alarm_cond) is False:
                    self.__light_one_rgb_color(AnimationExecutor._RED_COLOR, 0)
                    self.__light_mode_color(AnimationExecutor._RED_MODE, AnimationExecutor._OFF)
                    continue

                self.__light_one_rgb_color(AnimationExecutor._RED_COLOR, 254)
                self.__light_mode_color(AnimationExecutor._RED_MODE, AnimationExecutor._ON)
                self.__light_one_rgb_color(AnimationExecutor._RED_COLOR, 0)
                self.__light_mode_color(AnimationExecutor._RED_MODE, AnimationExecutor._OFF)

    def __warning_animation(self, warning_type):
        if warning_type == RESOURCE_PROVIDER.AC_TEMPERATURE_WARNING_ON:
            self.__turn_on_the_mode(AnimationExecutor._YELLOW_MODE)
        elif warning_type == RESOURCE_PROVIDER.AC_TEMPERATURE_WARNING_OFF:
            self.__turn_off_the_mode(AnimationExecutor._YELLOW_MODE)
        if warning_type == RESOURCE_PROVIDER.AC_HUMIDITY_WARNING_ON:
            self.__turn_on_the_mode(AnimationExecutor._GREEN_MODE)
        elif warning_type == RESOURCE_PROVIDER.AC_HUMIDITY_WARNING_OFF:
            self.__turn_off_the_mode(AnimationExecutor._GREEN_MODE)
        if warning_type == RESOURCE_PROVIDER.AC_MOTION_ENABLED:
            self.__turn_on_the_mode(AnimationExecutor._BLUE_MODE)
        elif warning_type == RESOURCE_PROVIDER.AC_MOTION_DISABLED:
            self.__turn_off_the_mode(AnimationExecutor._BLUE_MODE)

    def __main_animation(self):
        self.__alarm_enabled_lock.acquire()
        condition = self.__alarm_enabled
        self.__alarm_enabled_lock.release()

        if bool(condition) is True:
            self.__turn_all_off()
            return

        # warning animations
        self.__warning_type_lock.acquire()
        warning_type = self.__warning_type
        self.__warning_type_lock.release()
        if warning_type is not None:
            self.__warning_animation(warning_type)

        self.__light_one_rgb_color(
            AnimationExecutor._GREEN_COLOR,
            int((random.random() * 1000) % 254)
        )
        time.sleep(300.0 / 1000.0)
        self.__light_one_rgb_color(
            AnimationExecutor._BLUE_COLOR,
            int((random.random() * 1000) % 254)
        )
        time.sleep(300.0 / 1000.0)
        self.__light_one_rgb_color(
            AnimationExecutor._RED_COLOR,
            int((random.random() * 1000) % 254)
        )
        time.sleep(300.0 / 1000.0)
