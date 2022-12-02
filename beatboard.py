from cvzone.HandTrackingModule import HandDetector
import cv2 as cv
import pygame as pg
import numpy as np
import imutils

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
        self.old_freq = 0

    def detect_squares(self, img):
        # https://learnopencv.com/edge-detection-using-opencv/

        # Grayscale and Gaussian Blur
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_blur = cv.GaussianBlur(img_gray, (3, 3), 0)

        # Canny Edge Detection
        edges = cv.Canny(image=img_blur, threshold1=100,
                         threshold2=200)

        return edges
