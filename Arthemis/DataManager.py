"""
Data Manager module
"""
import threading
import time
import ScannerDataProvider
import DatabaseManager
import ResourceProvider

RESOURCE_PROVIDER = ResourceProvider.ResourceProvider()

class DataManager(threading.Thread):
    """
    Data Manager class
    """

    def __init__(self, database_name):
        threading.Thread.__init__(self)
        self.__scanner_data_provider = None
        self.__database_name = database_name
        self.__database_manager = None
        self.__is_running = False
        self.__running_lock = threading.Lock()
        self.__thread_timer = 0
        self.__data_timer = 0

    def run(self):
        self.__database_manager = DatabaseManager.DatabaseManager(self.__database_name)
        self.__scanner_data_provider = ScannerDataProvider.ScannerDataProvider()
        self.__scanner_data_provider.start()
        self.__running_lock.acquire()
        self.__is_running = True
        self.__running_lock.release()
        self.__thread_timer = time.time()
        self.__data_timer = time.time()
        while True:
            if time.time() - self.__thread_timer > 1000.0 / 1000.0:
                self.__running_lock.acquire()
                condition = self.__is_running
                self.__running_lock.release()
                if bool(condition) is False:
                    break
                self.__thread_timer = time.time()

            if time.time() - self.__data_timer > 100.0 / 1000.0:
                self.__store_in_db()
                self.__data_timer = time.time()

        # Wait for the threads to stop
        self.__scanner_data_provider.stop()
        self.__scanner_data_provider.join()

    def stop(self):
        """
        Stop
        """
        self.__running_lock.acquire()
        self.__is_running = False
        self.__running_lock.release()

    def __store_in_db(self):
        # Store data from Scanner into Database
        dict_scanner_data = self.__scanner_data_provider.get_scanner_data()

        if len(dict_scanner_data) > 0:
            # distance value
            values_list = dict_scanner_data.get('distance')
            # temperature value
            values_list = dict_scanner_data.get('temperature')
            if values_list:
                self.__database_manager.insert_data_in_database(values_list, \
                    'HOME_SCANNER_DATABASE_TEMPERATURE')
            # motion value
            values_list = dict_scanner_data.get('motion')
            if values_list:
                self.__database_manager.insert_data_in_database(values_list, \
                    'HOME_SCANNER_DATABASE_MOTION')
            # humidity value
            values_list = dict_scanner_data.get('humidity')
            if values_list:
                self.__database_manager.insert_data_in_database(values_list, \
                    'HOME_SCANNER_DATABASE_HUMIDITY')
            # gas value
            values_list = dict_scanner_data.get('gas')
            if values_list:
                self.__database_manager.insert_data_in_database(values_list, \
                    'HOME_SCANNER_DATABASE_GAS_RECORD')
            # light value
            values_list = dict_scanner_data.get('light')
            if values_list:
                self.__database_manager.insert_data_in_database(values_list, \
                    'HOME_SCANNER_DATABASE_LIGHT')
