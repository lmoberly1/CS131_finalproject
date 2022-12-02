from cvzone.HandTrackingModule import HandDetector
import cv2 as cv
import pygame as pg
import numpy as np
import imutils
from frame_ops import FrameOperations

notes = [
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C"]


def synth(frequency=261, duration=1.5, sampling_rate=44100):
    frames = int(duration*sampling_rate)
    arr = np.cos(2*np.pi*frequency*np.linspace(0, duration, frames))
    arr = arr + np.cos(4*np.pi*frequency *
                       np.linspace(0, duration, frames))
    arr = arr - np.cos(6*np.pi*frequency *
                       np.linspace(0, duration, frames))
    # arr = np.clip(arr*10, -1, 1) # squarish waves
    # arr = np.cumsum(np.clip(arr*10, -1, 1)) # triangularish waves pt1
    # arr = arr+np.sin(2*np.pi*frequency*np.linspace(0,duration, frames)) # triangularish waves pt1
    arr = arr/max(np.abs(arr))  # triangularish waves pt1
    sound = np.asarray([32767*arr, 32767*arr]).T.astype(np.int16)
    sound = pg.sndarray.make_sound(sound.copy())

    return sound


class Beatboard():

    def __init__(self):
        self.detector = HandDetector(detectionCon=0.8)
        self.FRAME_OPS = FrameOperations()
        self.old_freq = 0

    def extract_shape(self, cell):
        """
        Parameters:
        -
        Returns:
        -
        """
        pass

    def detect_grid(self, img):
        """
        Parameters:
        - img: image containing grid
        Returns:
        - 2-tuple of grid in both RGB and grayscale
        """

        # Grayscale and Gaussian Blur
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_blur = cv.GaussianBlur(img_gray, (3, 3), 0)

        # Canny Edge Detection
        # edges = cv.Canny(image=img_blur, threshold1=100,
        #                  threshold2=200)

        # Adaptive Thresholding
        thresh = cv.adaptiveThreshold(img_blur, 255,
                                      cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
        thresh = cv.bitwise_not(thresh)

        # Contour Detection
        contours, _ = cv.findContours(
            thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        contours = sorted(contours, key=cv.contourArea, reverse=True)

        # Find Grid Outline
        gridOutline = None
        # Loop over the contours
        for c in contours:
            # Approximate the contour
            peri = cv.arcLength(c, True)
            approx = cv.approxPolyDP(c, 0.02 * peri, True)
            # If contour has 4 points, assume we have found grid outline
            if len(approx) == 4:
                gridOutline = approx
                break

        if gridOutline is None:
            raise Exception(
                ("Could not find grid outline. Debug thresholding and contour steps."))

        grid = self.FRAME_OPS.four_point_transform(
            img, gridOutline.reshape(4, 2))
        gray_grid = self.FRAME_OPS.four_point_transform(
            img_gray, gridOutline.reshape(4, 2))

        return (grid, gray_grid)


"""
img_copy = img.copy()
for c in contours:
    x, y, w, h = cv.boundingRect(c)
    cv.putText(img_copy, str(w), (x, y - 10),
                cv.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    cv.rectangle(img_copy, (x, y), (x + w, y + h), (36, 255, 12), 1)

# cv.drawContours(img_copy, contours, -1, (0, 255, 0), 2)
cv.imshow("Puzzle Outline", img_copy)
cv.waitKey(0)

Grid out
        # output = img.copy()
        # cv.drawContours(output, [gridOutline], -1, (0, 255, 0), 2)
        # cv.imshow("Puzzle Outline", output)
        # cv.waitKey(0)
"""
