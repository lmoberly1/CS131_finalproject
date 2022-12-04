from cvzone.HandTrackingModule import HandDetector
import cv2 as cv
import pygame as pg
import numpy as np


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


def get_freq(dist):
    freq = 0
    note_text = 'A'
    if dist < 100:  # c5
        freq = 523
        note_text = 'C'
    if dist < 200:  # b4
        freq = 494
        note_text = 'B'
    elif dist < 300:  # a4
        freq = 440
        note_text = 'A'
    elif dist < 400:  # g4
        freq = 392
        note_text = 'G'
    elif dist < 500:  # f4
        freq = 349
        note_text = 'F'
    elif dist < 600:  # e4
        freq = 330
        note_text = 'E'
    elif dist < 700:  # d4
        freq = 294
        note_text = 'D'
    else:  # c4
        freq = 263
        note_text = 'C'
    return freq, note_text


class Trombone():

    def __init__(self):
        self.detector = HandDetector(detectionCon=0.8)
        self.old_freq = 0

    def play(self, frame, x1, x2, hand_height):
        # play sound because hand is closed
        if hand_height < 250:
            dist = abs(x2 - x1)
            freq = 0
            note_text = 'A'

            freq, note_text = get_freq(dist)

            if self.old_freq != freq:
                pg.mixer.stop()
                self.old_freq = freq
                sound = synth(freq, 3)
                cv.putText(frame, note_text, (100, 100),
                           cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5)
                sound.play()
        else:
            pg.mixer.stop()
        return frame

    def detect(self, frame):
        hands, img = self.detector.findHands(frame)

        if hands:
            # Hand 1
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # List of 21 Landmark points
            bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
            centerPoint1 = hand1['center']  # center of the hand cx,cy
            handType1 = hand1["type"]  # Handtype Left or Right
            # Hand 2
            if len(hands) > 1:
                hand2 = hands[1]
                lmList2 = hand2["lmList"]  # List of 21 Landmark points
                bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
                centerPoint2 = hand2['center']  # center of the hand cx,cy
                handType2 = hand2["type"]  # Handtype Left or Right
                hand_height = bbox2[3] if bbox2[3] < bbox1[3] else bbox1[3]
                self.play(frame, centerPoint1[0], centerPoint2[0], hand_height)
        return img
