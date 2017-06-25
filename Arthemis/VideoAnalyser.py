"""
MP4 Video Analyser module
"""

import os
import cv2
import numpy
import sys

class VideoAnalyser(object):
    """
    MP4 Video Analyser class - responsible to analyse the mp4 files recorded
    and apply detections
    """
    def __init__(self):
        self.__detections_applied = False
        self.__faces_positions = []
        self.__motion_positions = []
        self.__human_positions = []

        self.__face_detect_enabled = False
        self.__motion_detect_enabled = False
        self.__human_detect_enabled = False

        self.__analysed_file_name = None

        self.__face_cascade = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml"
        )

    def enable_face_recognition(self, enable):
        """
        analyse the given mp4 file
        """
        if enable > 0:
            self.__face_detect_enabled = True
        else:
            self.__face_detect_enabled = False

    def enable_motion_detection(self, enable):
        """
        analyse the given mp4 file
        """
        if enable > 0:
            self.__motion_detect_enabled = True
        else:
            self.__motion_detect_enabled = False

    def enable_human_recognition(self, enable):
        """
        analyse the given mp4 file
        """
        if enable > 0:
            self.__human_detect_enabled = True
        else:
            self.__human_detect_enabled = False

    def apply_detections(self, mp4_file_name):
        """
        Apply the detections results + rewrite the original file
        """
        cap = cv2.VideoCapture(str(mp4_file_name))
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        out_file = cv2.VideoWriter(
            os.path.splitext(mp4_file_name)[0] + '.avi',
            fourcc,
            25.0,
            (1920, 1080)
        )

        while cap.isOpened():
            ret, frame = cap.read()

            if bool(ret) is False:
                break

            frame = cv2.flip(frame, 0)

            if bool(self.__face_detect_enabled) is True:
                self.__face_detection_algorithm(frame)
                self.__detections_applied = True

            if bool(self.__motion_detect_enabled) is True:
                self.__motion_detection_algorithm(frame)
                self.__detections_applied = True

            if bool(self.__human_detect_enabled) is True:
                self.__human_detection_algorithm(frame)
                self.__detections_applied = True

            if bool(self.__detections_applied) is True:
                self.__apply_detections(frame)
                self.__detections_applied = False

            out_file.write(frame)

    def __face_detection_algorithm(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.__face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        self.__faces_positions = faces

    def __motion_detection_algorithm(self, frame):
        print 'motion'

    def __human_detection_algorithm(self, frame):
        print 'human'

    def __apply_detections(self, frame):
        if bool(self.__face_detect_enabled) is True:
            for (x_coord, y_coord, width, height) in self.__faces_positions:
                cv2.rectangle(
                    frame,
                    (x_coord, y_coord),
                    (x_coord + width, y_coord + height),
                    (0, 255, 0),
                    2
                )
            self.__faces_positions = []
