"""
Animation Executor module
"""

import time
import SerialManager
import ResourceProvider

RESOURCE_PROVIDER = ResourceProvider.ResourceProvider()

class AnimationExecutor(object):
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
        self.__serial_manager = None
        self.__connect_to_board()

    def __connect_to_board(self):
        board_ratio = RESOURCE_PROVIDER.get_string_table('ANIMATOR_BOARD_RATIO')
        anim_board = RESOURCE_PROVIDER.get_string_table('ANIMATOR_BOARD')
        board_name = RESOURCE_PROVIDER.get_board_name(anim_board)
        if board_name and board_ratio:
            self.__serial_manager = SerialManager.SerialManager(board_name, int(board_ratio))
            return True
        else:
            return False

    def execute(self, animation_command):
        """
        execute the giben animation command
        """
        print animation_command

    def turn_on_the_mode(self, mode_color):
        """
        turn on the led for a specific mode
        """
        self.__light_mode_color(mode_color, AnimationExecutor._ON)

    def turn_off_the_mode(self, mode_color):
        """
        turn off the led for a specific mode
        """
        self.__light_mode_color(mode_color, AnimationExecutor._OFF)

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

    def __turn_all_off(self):
        self.__custom_anim_lock.acquire()
        self.__custom_animation_on = False
        self.__custom_anim_lock.release()
        self.__light_one_rgb_color(AnimationExecutor._RED_COLOR, 0)
        self.__light_mode_color(AnimationExecutor._BLUE_MODE, AnimationExecutor._OFF)
        self.__light_mode_color(AnimationExecutor._RED_MODE, AnimationExecutor._OFF)
        self.__light_one_rgb_color(AnimationExecutor._GREEN_COLOR, 0)
        self.__light_one_rgb_color(AnimationExecutor._BLUE_COLOR, 0)
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

    def __alarm_animation(self):
        self.__turn_all_off()
        while True:
            self.__alarm_lock.acquire()
            alarm_cond = self.__alarm_on
            self.__alarm_lock.release()

            if bool(alarm_cond) is False:
                self.__turn_all_off()
                break

            self.__light_one_rgb_color(AnimationExecutor._RED_COLOR, 254)
            self.__light_mode_color(AnimationExecutor._RED_MODE, AnimationExecutor._ON)
            self.__light_one_rgb_color(AnimationExecutor._RED_COLOR, 0)
            self.__light_mode_color(AnimationExecutor._RED_MODE, AnimationExecutor._OFF)

    def __main_animation(self):
        if bool(self.__main_anim_turned_on) is False:
            self.__light_one_rgb_color(AnimationExecutor._GREEN_COLOR, 254)
            self.__light_one_rgb_color(AnimationExecutor._BLUE_COLOR, 254)
            #self.__light_one_rgb_color(AnimationExecutor._GREEN_COLOR, 0)
            #self.__light_one_rgb_color(AnimationExecutor._BLUE_COLOR, 0)

    def __startup_animation(self):
        self.__turn_all_off()
        command = []
        self.__do_animation(command)
        self.__turn_all_off()

    def __custom_animation(self):
        self.__turn_all_off()
        command = []
        self.__do_animation(command)
