"""
Data Manager module
"""
import threading
import time
import SerialManager
import DatabaseManager
import DataProvider

DATA_PROVIDER = DataProvider.DataProvider()

class DataManager(threading.Thread):
    """
    Data Manager class
    """

    def __init__(self, database_name):
        threading.Thread.__init__(self)
        self.__serial_manager = None
        self.__database_name = database_name
        self.__database_manager = None
        self.__is_running = False
        self.__running_lock = threading.Lock()
        self.__thread_timer = 0

    def __connect_to_board(self):
        board_ratio = DATA_PROVIDER.get_string_table(DATA_PROVIDER.SCANNER_BOARD_RATIO)
        scanner_board = DATA_PROVIDER.get_string_table(DATA_PROVIDER.SCANNER_BOARD)
        board_name = DATA_PROVIDER.get_board_name(scanner_board)
        if board_name and board_ratio:
            self.__serial_manager = SerialManager.SerialManager(board_name, int(board_ratio))
            return True
        else:
            return False

    def run(self):
        # Start the Serial Manager thread for reading
        self.__database_manager = DatabaseManager.DatabaseManager(self.__database_name)
        if bool(self.__connect_to_board()) is False:
            return
        self.__serial_manager.start()
        self.__running_lock.acquire()
        self.__is_running = True
        self.__running_lock.release()
        self.__thread_timer = time.time()
        while True:
            if time.time() - self.__thread_timer > 200.0 / 1000.0:
                self.__store_in_db()
                self.__running_lock.acquire()
                condition = self.__is_running
                self.__running_lock.release()
                if bool(condition) is False:
                    break
                self.__thread_timer = time.time()

    def stop(self):
        """
        Stop
        """
        # stop the Serial Manager thread
        self.__serial_manager.stop()
        # Wait for the threads to stop
        self.__serial_manager.join()
        self.__running_lock.acquire()
        self.__is_running = False
        self.__running_lock.release()

    def get_data(self):
        """
        Get scanner data
        """
        return self.__serial_manager.get_scanner_data()

    def __store_in_db(self):
        # Store data from Serial into Database
        dict_scanner_data = self.__serial_manager.get_scanner_data()

        if len(dict_scanner_data) <= 0:
            return

        #we will use this data only for surveillance mode
        values_list = [dict_scanner_data.get('distance'), \
            dict_scanner_data.get('time_collected')]
        self.__database_manager.insert_data_in_database(values_list, \
            'HOME_SCANNER_DATABASE_DISTANCE')

        values_list = [dict_scanner_data.get('temperature'), \
            dict_scanner_data.get('time_collected')]
        self.__database_manager.insert_data_in_database(values_list, \
            'HOME_SCANNER_DATABASE_TEMPERATURE')

        values_list = [dict_scanner_data.get('motion'), \
            dict_scanner_data.get('time_collected')]
        self.__database_manager.insert_data_in_database(values_list, \
            'HOME_SCANNER_DATABASE_MOTION')

        values_list = [dict_scanner_data.get('humidity'), \
            dict_scanner_data.get('time_collected')]
        self.__database_manager.insert_data_in_database(values_list, \
            'HOME_SCANNER_DATABASE_HUMIDITY')

        values_list = [dict_scanner_data.get('gas'), \
            dict_scanner_data.get('time_collected')]
        self.__database_manager.insert_data_in_database(values_list, \
            'HOME_SCANNER_DATABASE_GAS_RECORD')

        values_list = [dict_scanner_data.get('light'), \
            dict_scanner_data.get('time_collected')]
        self.__database_manager.insert_data_in_database(values_list, \
            'HOME_SCANNER_DATABASE_LIGHT')
