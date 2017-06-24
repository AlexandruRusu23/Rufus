"""
MP4 Video Analyser module
"""

class VideoAnalyser(object):
    """
    MP4 Video Analyser class - responsible to analyse the mp4 files recorded
    and apply detections
    """
    def __init__(self):
        self.__my_var = 0
        self.__faces_positions = []
        self.__motion_positions = []
        self.__human_positions = []

        self.__analysed_file_name = None

    def face_recognition(self, mp4_file_name):
        """
        analyse the given mp4 file
        """
        print 'face'

    def motion_detection(self, mp4_file_name):
        """
        analyse the given mp4 file
        """
        print 'motion'

    def human_recognition(self, mp4_file_name):
        """
        analyse the given mp4 file
        """
        print 'human'

    def apply_detections(self, mp4_file_name):
        """
        Apply the detections results + rewrite the original file
        """
        print 'apply'
