import os
import cv2 as cv
import numpy as np
import pygame as pg
from time import sleep

# Contains sound operations


class SoundOperations():

    def __init__(self):
        pass
        self.notes = [
            "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C"]
        self.midi_numbers = [72, 71, 69, 67, 65,
                             64, 62, 60]  # C5 to C4 in MIDI numbers
        self.instrument_numbers = {
            1: 38,  # circle = bass
            3: 115,  # triangle = woodblock
            4: 47,  # square = timpani
            5: 0,
            6: 0,
        }

    def play_midi(self, player, beats, length, volume):
        """
        Parameters:
        - player: pygame midi output
        - instruments: 1D int array; int corresponds to instrument type (1, 3, 4, 5, or 6)
        - length: duration sound will be played
        - volume: volume of sound (max is 127)
        """
        notes = []
        for note_index, instrument_index in enumerate(beats):
            if instrument_index:
                # Get note and instrument
                instrument = self.instrument_numbers[instrument_index]
                note = self.midi_numbers[note_index]
                notes.append(note)
                print('TURNING NOTE ON')
                player.noteon(0, 60, 30)
                player.noteon(0, 67, 30)
                player.noteon(0, 76, 30)
              # player.note_on(note, volume)

        sleep(length)
        for n in notes:
            player.note_off(n, volume)
        sleep(length)
