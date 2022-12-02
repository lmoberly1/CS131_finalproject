import cv2 as cv
from frame_ops import FrameOperations
from distance_between import DistanceEstimator
from trombone import Trombone
from beatboard import Beatboard
import pygame as pg


class VideoManager():

    def __init__(self):
        self.DISTANCE_ESTIMATOR = DistanceEstimator()
        self.TROMBONE = Trombone()  # trombone
        self.BEATBOARD = Beatboard()  # piano
        self.FRAME_OPS = FrameOperations()

        self.FIRST = True

    def estimate_vid(self, webcam_id=0):
        """
        Reads webcam, applies distance estimation on webcam
        """
        cap = cv.VideoCapture(webcam_id)
        cap.set(3, 1920)
        cap.set(4, 1080)

        pg.init()
        pg.mixer.init()

        # img = cv.imread('test.jpeg')
        # frame = self.BEATBOARD.detect_squares(img)
        # cv.imwrite('hough.jpg', frame)

        while(True):
            has_frame, frame = cap.read()
            # frame = cv.flip(frame, 1)
            # cv.waitKey(200)

            if self.FIRST:
                self.WEB_CAM_H, self.WEB_CAM_W = frame.shape[0:2]
                self.FIRST = False

            # frame = self.TROMBONE.detect(frame)
            frame = self.BEATBOARD.detect_squares(frame)
            cv.imshow('frame', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
