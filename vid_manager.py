import cv2 as cv
from frame_ops import FrameOperations
from trombone import Trombone
from beatboard import Beatboard
import pygame as pg


class VideoManager():

    def __init__(self):
        self.TROMBONE = Trombone()  # trombone
        self.BEATBOARD = Beatboard()  # piano
        self.FRAME_OPS = FrameOperations()
        self.FIRST = True

    def estimate_img(self):

        img = cv.imread('grid.jpeg')
        grid_rgb, grid_gray = self.BEATBOARD.detect_grid(img)
        cv.imwrite('grid_lines.jpg', grid_gray)

    def estimate_vid(self, webcam_id=0):

        cap = cv.VideoCapture(webcam_id)
        cap.set(3, 1920)
        cap.set(4, 1080)

        pg.init()
        pg.mixer.init()

        while(True):
            has_frame, frame = cap.read()
            # frame = cv.flip(frame, 1)
            # cv.waitKey(200)

            if self.FIRST:
                self.WEB_CAM_H, self.WEB_CAM_W = frame.shape[0:2]
                self.FIRST = False

            # frame = self.TROMBONE.detect(frame)
            grid_rgb, grid_gray = self.BEATBOARD.detect_grid(img)
            cv.imshow('frame', grid_rgb)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
