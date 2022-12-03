import os
import cv2 as cv
import numpy as np
import pygame as pg


# Contains sound operations
class SoundOperations():

    def __init__(self):
        pass
        self.notes = [
            "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C"]

    def get_sound(self, frequency=263, duration=1.5, sampling_rate=44100):
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
