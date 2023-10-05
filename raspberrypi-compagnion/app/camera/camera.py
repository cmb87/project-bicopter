import time
import cv2
import logging
import numpy as np
import config
from .decoder import decode

class Camera:
    def __init__(self):
        """
        The videoplayer object combines the tflite model with opencv2 camera reading function
        """

        self.cap = cv2.VideoCapture(int(config.analytic["source"]))


    # ================================
    def processFrame(self):
        """
        Processes frame by frame
        :return:
        """

        while True:
            logging.debug("Processing frame")
            ret, frame = self.cap.read()

            if config.analytic['graysend'] == "1":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame = cv2.resize(frame, (config.analytic["send_width"], config.analytic["send_height"]))

            if config.analytic["flip"] == "1":
                frame = cv2.flip(frame, 0)

            if frame is not None:
                yield (decode(frame), None, None)
