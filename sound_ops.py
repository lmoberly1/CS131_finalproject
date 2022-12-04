import os
import cv2 as cv
import numpy as np
import pygame as pg


class SoundOperations():

    def __init__(self):
        pass
        self.notes = [
            "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C"]
        self.midi_numbers = [72, 71, 69, 67, 65,
                             64, 62, 60]  # C5 to C4 in MIDI numbers

        pg.init()
        pg.mixer.init()

        self.hi_hat = pg.mixer.Sound('sounds/hi_hat.wav')
        self.snare = pg.mixer.Sound('sounds/snare.wav')
        self.kick = pg.mixer.Sound('sounds/kick.wav')
        self.crash = pg.mixer.Sound('sounds/crash.wav')
        self.clap = pg.mixer.Sound('sounds/clap.wav')
        self.tom = pg.mixer.Sound("sounds/tom.wav")

        self.instrument_numbers = {
            0: self.hi_hat,
            1: self.hi_hat,
            2: self.hi_hat,
            3: self.snare,
            4: self.kick,
            5: self.crash,
            6: self.clap,
            7: self.tom
        }

    def play_sounds(self, beats, length):
        """
        Parameters:
        - player: pygame midi output
        - instruments: 1D int array; int corresponds to instrument type (1, 3, 4, 5, or 6)
        - length: duration sound will be played
        Function:
        - plays all notes on one beat
        """
        for instrument_index, other_index in enumerate(beats):
            if other_index:  # there is a sound
                print('Playing note: ', instrument_index)
                instrument = self.instrument_numbers[instrument_index]
                instrument.play()
