from vid_manager import VideoManager
from sound_ops import SoundOperations
import os


class Main():

    def __init__(self):
        self.VI_M = VideoManager()
        self.SOUND = SoundOperations()

    def live_estimation(self, webcam_id=0):
        self.VI_M.estimate_vid(webcam_id)

    def music(self):
        self.SOUND.play_sound()


if __name__ == "__main__":
    app = Main()
    app.music()
    # app.live_estimation(0)
