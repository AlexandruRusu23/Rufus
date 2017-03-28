"""
Data Provider Module
"""
import os
import yaml

class DataProvider(object):
    """
    Data Provider Class
    """
    def __init__(self):
        self.__string_table = yaml.load(open('Strings.txt', 'r'))
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

    def clear_data(self):
        """
        Clear Data
        """
        self._scanner_board_name = ''
        self._animator_board_name = ''

    def find_all_devices(self):
        """
        Find All Devices
        """
        self.__find_device(self.get_string_table('SCANNER_BOARD'))
        self.__find_device(self.get_string_table('ANIMATOR_BOARD'))
        print self._scanner_board_name
        print self._animator_board_name

    def __find_device(self, board_type):
        """
        Find a specific device
        """
        self.clear_data()
        path_string = self.get_string_table('PATH_ARDUINO_BOARDS')
        files_to_search_in = os.listdir(path_string)
        file_substr = self.get_string_table('SUBSTR_ANIMATOR_FILE')
        if board_type == self.get_string_table('SCANNER_BOARD'):
            file_substr = self.get_string_table('SUBSTR_SCANNER_FILE')
        for current_file in files_to_search_in:
            if file_substr in current_file:
                self._scanner_board_name = current_file
