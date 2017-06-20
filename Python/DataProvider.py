"""
Data Provider Module
"""
import os
import yaml

class DataProvider(object):
    """
    Data Provider Class
    """
    RESOURCE_FILE = 'Strings.txt'
    SCANNER_BOARD_RATIO = 'SCANNER_BOARD_RATIO'
    SCANNER_BOARD = 'SCANNER_BOARD'
    ANIMATOR_BOARD = 'ANIMATOR_BOARD'
    PATH_ARDUINO_BOARDS = 'PATH_ARDUINO_BOARDS'
    SUBSTR_ANIMATOR_FILE = 'SUBSTR_ANIMATOR_FILE'
    SUBSTR_SCANNER_FILE = 'SUBSTR_SCANNER_FILE'
    CAMERA_FRAMERATE = 'CAMERA_FRAMERATE'
    CAMERA_DURATION = 'CAMERA_DURATION'

    def __init__(self):
        self.__string_table = yaml.load(open(DataProvider.RESOURCE_FILE, 'r'))
        self._scanner_board_name = ''
        self._animator_board_name = ''

    def get_string_table(self, string_name):
        """
        Get a string from resource dictionary giving the key of the dictionary \n
        If nothing found then an empty string will be returned
        """
        if string_name in self.__string_table.keys():
            return self.__string_table[string_name]
        else:
            return ''

    def get_board_name(self, board_type):
        """
        Get the name of a specific arduino board
        """
        self.__find_all_devices()
        if board_type == self.get_string_table(DataProvider.SCANNER_BOARD):
            return self._scanner_board_name
        if board_type == self.get_string_table(DataProvider.ANIMATOR_BOARD):
            return self._animator_board_name
        return ''

    def clear_data(self):
        """
        Clear Data
        """
        self._scanner_board_name = ''
        self._animator_board_name = ''

    def __find_all_devices(self):
        """
        Find All Devices
        """
        self.clear_data()
        self.__find_device(self.get_string_table(DataProvider.SCANNER_BOARD))
        self.__find_device(self.get_string_table(DataProvider.ANIMATOR_BOARD))

    def __find_device(self, board_type):
        """
        Find a specific device
        """
        path_string = self.get_string_table(DataProvider.PATH_ARDUINO_BOARDS)
        files_to_search_in = os.listdir(path_string)
        file_substr = self.get_string_table(DataProvider.SUBSTR_ANIMATOR_FILE)
        if board_type == self.get_string_table(DataProvider.SCANNER_BOARD):
            file_substr = self.get_string_table(DataProvider.SUBSTR_SCANNER_FILE)
        for current_file in files_to_search_in:
            if file_substr in current_file:
                if board_type == self.get_string_table(DataProvider.SCANNER_BOARD):
                    self._scanner_board_name = path_string + current_file
                else:
                    self._animator_board_name = path_string + current_file
