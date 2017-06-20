"""
Serial Manager Module
"""
import threading
import time
import datetime
import re
import serial

class SerialManager(threading.Thread):
    """
    Class implemented to manipulate the Microcontroller's Serial
    """
    def __init__(self, serial_name, serial_ratio):
        threading.Thread.__init__(self)
        self.__running_lock = threading.Lock()
        self.__scanner_dict_lock = threading.Lock()
        self.__serial_name = serial_name
        self.__serial_ratio = serial_ratio
        self.__serial_file = None
        self.__commands_list = []
        self.__dict_scanner_data = {}
        self.__is_running = False
        self.__thread_timer = 0

    def run(self):
        self.__running_lock.acquire()
        self.__is_running = True
        self.__running_lock.release()
        self.__serial_file = serial.Serial(self.__serial_name, self.__serial_ratio)
        self.__thread_timer = time.time()
        while True:
            if time.time() - self.__thread_timer > 100.0 / 1000.0:
                self.__reader()

                self.__running_lock.acquire()
                condition = self.__is_running
                self.__running_lock.release()
                if bool(condition) is False:
                    break
                self.__thread_timer = time.time()

        self.__serial_file.close()

    def __reader(self):
        """
        Method created to read from Microcontroller's Serial
        """
        line = self.__serial_file.readline()
        if line:
            if 'scanner_data' in line:
                line = self.__serial_file.readline()
                while 'end_scanner_data' not in line:
                    if line:
                        self.__store_in_dictionary(line)
                    line = self.__serial_file.readline()
            timest = time.time()
            timestamp = datetime.datetime.fromtimestamp(timest).strftime('%Y-%m-%d %H:%M:%S')
            self.__scanner_dict_lock.acquire()
            self.__dict_scanner_data['time_collected'] = timestamp
            self.__scanner_dict_lock.release()

    def __store_in_dictionary(self, line_to_store):
        """
        Convert from string to dictionary fields
        """
        line_to_store_tokenized = re.findall(r"[\w.]+", line_to_store)
        if len(line_to_store_tokenized) > 1:
            self.__dict_scanner_data[line_to_store_tokenized[0]] = line_to_store_tokenized[1]

    def __writer(self):
        """
        Method created to write on Microcontroller's Serial
        """
        for element in enumerate(self.__commands_list):
            if len(element) > 1:
                self.__serial_file.write(str(element[1]))
                time.sleep(100.0 / 1000.0)
        self.__commands_list = []

    def stop(self):
        """
        stop the Serial Manager
        """
        self.__running_lock.acquire()
        self.__is_running = False
        self.__running_lock.release()

    def get_scanner_data(self):
        """
        Get the data from Serial from a dictionary which is returned by the function
        """
        self.__scanner_dict_lock.acquire()
        output = self.__dict_scanner_data
        self.__dict_scanner_data = {}
        self.__scanner_dict_lock.release()
        return output

    def set_scanner_commands(self, commands_list):
        """
        send a list of commands for SerialManager to be send to Microcontroller
        """
        self.__commands_list = commands_list

    def execute_commands(self):
        """
        Send to Microcontroller's Serial the commands stored in __commands_list
        """
        self.__writer()
