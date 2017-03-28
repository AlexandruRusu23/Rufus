"""
 Engine module
"""
import DataProvider

class Engine(object):
    """
    Engine Class
    """

    data_provider = DataProvider.DataProvider() #static

    def __init__(self):
        print 'heello'
