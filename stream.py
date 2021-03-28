import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
from flask import Flask, render_template, Response, request
import threading
import os

class VideoCamera(object):
    def __init__(self, flip = True):
        self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
