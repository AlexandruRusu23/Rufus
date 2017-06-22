"""
Scanner Data Module
"""
import threading
import time
import Queue
import SerialManager
import ResourceProvider

RESOURCE_PROVIDER = ResourceProvider.ResourceProvider()

class ScannerDataProvider(threading.Thread):
    """
    ScannerDataProvider class
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.__serial_manager = None
        self.__data_timer = 0

        self.__is_running = False
        self.__is_running_lock = threading.Lock()
        self.__thread_timer = 0

        self.__scanner_data_queue = Queue.Queue(20)

    def __connect_to_board(self):
        board_ratio = RESOURCE_PROVIDER.get_string_table(RESOURCE_PROVIDER.SCANNER_BOARD_RATIO)
        scanner_board = RESOURCE_PROVIDER.get_string_table(RESOURCE_PROVIDER.SCANNER_BOARD)
        board_name = RESOURCE_PROVIDER.get_board_name(scanner_board)
        if board_name and board_ratio:
            self.__serial_manager = SerialManager.SerialManager(board_name, int(board_ratio))
            return True
        else:
            return False

    def run(self):
        """
        thread-run method
        """
        if bool(self.__connect_to_board()) is False:
            print '[ScannerDataProvider] Cant connect to SerialManager'
            return

        self.__serial_manager.start()
        self.__is_running_lock.acquire()
        self.__is_running = True
        self.__is_running_lock.release()
        while True:
            if time.time() - self.__thread_timer > 1000.0/1000.0:
                self.__is_running_lock.acquire()
                condition = self.__is_running
                self.__is_running_lock.release()
                if bool(condition) is False:
                    break

                self.__thread_timer = time.time()

            if time.time() - self.__data_timer > 100.0/1000.0:
                self.__store_data(self.__serial_manager.get_scanner_data())
                self.__data_timer = time.time()

        self.__serial_manager.stop()
        self.__serial_manager.join()

    def stop(self):
        """
        stop the main thread
        """
        self.__is_running_lock.acquire()
        self.__is_running = False
        self.__is_running_lock.release()

    def __store_data(self, scanner_data_dict):
        try:
            self.__scanner_data_queue.put(scanner_data_dict, False)
        except Queue.Full:
            pass

    def get_scanner_data(self):
        """
        get scanner data
        """
        try:
            output = self.__scanner_data_queue.get(False)
        except Queue.Empty:
            return {}

        return output
