"""
Scanner Data Analyser module
"""
import UserCmdProvider

class DataAnalyser(object):
    """
    Scanner Data Analyser class - responsible to analyse the scanner data
    and return feedback, also commands for Animation Manager
    """
    def __init__(self):
        self.__user_cmd_provider = None
        self.__notifications_list = []
        self.__motion_status = False

    def analyse(self, scanner_data_dict, animations_cmd_queue):
        """
        Analyse the given dictionary
        """
        self.__user_cmd_provider = UserCmdProvider.UserCmdProvider()
        scanner_data = scanner_data_dict.get(False)
        print scanner_data
        animations_cmd_queue.put('1/2/2/1/', False)

    def motion_status(self):
        """
        returns True if motion has been detected and False otherwise
        """
        return self.__motion_status

    def get_notifications(self):
        """
        get the possible notifications
        """
        return self.__notifications_list
