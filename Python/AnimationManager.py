"""
Animation Manager module
"""
import threading
import time
import SerialManager
import DataProvider

class AnimationManager(threading.Thread):
    """
    Animation Manager class
    """

    data_provider = DataProvider.DataProvider() #static

    def __init__(self):
        threading.Thread.__init__(self)
        board_ratio = AnimationManager.data_provider.get_string_table('ANIMATOR_BOARD_RATIO')
        board_name = AnimationManager.data_provider.get_board_name('ANIMATOR_BOARD')
        self.__serial_manager = SerialManager.SerialManager(board_name, int(board_ratio))
        self.__alarm_on = False
        self.__thread_lock = threading.Lock()
        self.__running_lock = threading.Lock()
        self.__serial_lock = threading.Lock()
        self.__is_running = True
        self.__main_anim_on = False
        self.__turn_off = False

    def run(self):
        time.sleep(0.5)
        self.__startup_effect()
        while True:
            self.__running_lock.acquire()
            if bool(self.__is_running) is False:
                self.__running_lock.release()
                break
            self.__running_lock.release()
            self.__main_animation()
            self.__alarm_effect()
            time.sleep(1)

    def stop(self):
        """
        Stop method
        """
        self.__running_lock.acquire()
        self.__is_running = False
        self.__running_lock.release()
        self.stop_the_alarm()
        self.__turn_all_off()

    def __light_one_color(self, color_str, intensity, timeout):
        color_int = 11 #blue by default
        if color_str == 'red':
            color_int = 9
        if color_str == 'green':
            color_int = 10
        self.__serial_lock.acquire()
        aux_string = AnimationManager.data_provider.get_string_table('ANALOG_WRITE')
        aux_string = aux_string + str(color_int) + '/' + str(intensity)+ '/'
        self.__serialManager.write(aux_string)
        self.__serial_lock.release()
        time.sleep(timeout)

    def __light_mode_color(self, color_str, intensity, timeout):
        color_int = 5 #green mode by default
        if color_str == 'yellow':
            color_int = 4
        if color_str == 'red':
            color_int = 3
        if color_str == 'blue':
            color_int = 2
        self.__serial_lock.acquire()
        aux_string = AnimationManager.data_provider.get_string_table('DIGITAL_WRITE')
        aux_string = aux_string + str(color_int) + '/' + str(intensity)+ '/'
        self.__serialManager.write(aux_string)
        self.__serial_lock.release()
        time.sleep(timeout)

    def __turn_all_off(self):
        if bool(self.__turn_off) is False:
            self.__turn_off = True
            self.__main_anim_on = False
            self.__light_one_color('red', 0, 0.1)
            self.__light_mode_color('blue', 0, 0.1)
            self.__light_mode_color('red', 0, 0.1)
            self.__light_one_color('green', 0, 0.1)
            self.__light_one_color('blue', 0, 0.1)
            self.__light_mode_color('yellow', 0, 0.1)
            self.__light_mode_color('green', 0, 0.1)

    def __startup_effect(self):
        contor = 5
        while contor > 0:
            contor = contor - 1

            self.__light_mode_color('red', 1, 0.1)
            self.__light_one_color('red', 255, 0.1)
            self.__light_mode_color('blue', 1, 0.1)
            self.__light_one_color('red', 0, 0.1)
            self.__light_one_color('green', 255, 0.1)
            self.__light_mode_color('blue', 0, 0.1)
            self.__light_mode_color('red', 0, 0.1)
            self.__light_mode_color('yellow', 1, 0.1)
            self.__light_one_color('green', 0, 0.1)
            self.__light_one_color('blue', 255, 0.1)
            self.__light_mode_color('green', 1, 0.1)
            self.__light_one_color('blue', 0, 0.1)
            self.__light_mode_color('yellow', 0, 0.1)
            self.__light_mode_color('green', 0, 0.1)

    def __alarm_effect(self):
        while True:
            self.__thread_lock.acquire()
            if bool(self.__alarm_on) is False:
                self.__thread_lock.release()
                self.__turn_off = False
                break
            self.__thread_lock.release()
            self.__turn_all_off()
            self.__light_one_color('red', 255, 0.1)
            self.__light_mode_color('red', 1, 0.1)
            self.__light_one_color('red', 0, 0.1)
            self.__light_mode_color('red', 0, 0.1)

    def __main_animation(self):
        if bool(self.__main_anim_on) is False:
            self.__main_anim_on = True
            self.__light_one_color('green', 255, 0.1)
            self.__light_one_color('blue', 255, 0.1)

    def ring_the_alarm(self):
        """
        Ring The Alarm
        """
        self.__thread_lock.acquire()
        self.__alarm_on = True
        self.__thread_lock.release()

    def stop_the_alarm(self):
        """
        Stop the Alarm
        """
        self.__thread_lock.acquire()
        self.__alarm_on = False
        self.__thread_lock.release()

    def turn_on_the_mode(self, mode_color):
        """
        turn on the led for a specific mode
        """
        self.__light_mode_color(mode_color, 1, 0.1)

    def turn_off_the_mode(self, mode_color):
        """
        turn off the led for a specific mode
        """
        self.__light_mode_color(mode_color, 0, 0.1)
