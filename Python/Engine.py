"""
 Engine module
"""
import DataProvider
import DataManager

class Engine(object):
    """
    Engine Class
    """

    data_provider = DataProvider.DataProvider() #static

    def __init__(self):
        self.__data_manager = DataManager.DataManager('test_create_DB')

    def start(self):
        """
        start
        """
        self.__data_manager.start()

    def stop(self):
        """
        stop
        """
        self.__data_manager.stop()
