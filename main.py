from vid_manager import VideoManager
import os


class Main():

    def __init__(self):
        self.VI_M = VideoManager()

    def live_estimation(self, webcam_id=0, bpm=240, program='beatboard'):
        self.VI_M.estimate_vid(webcam_id, bpm, program)

    def img_estimation(self):
        self.VI_M.estimate_img()


if __name__ == "__main__":
    app = Main()
    app.live_estimation()
    # app.img_estimation()
