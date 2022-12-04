from vid_manager import VideoManager
import os


class Main():

    def __init__(self):
        self.VI_M = VideoManager()

    def live_estimation(self, webcam_id=0, bpm=240, setup=False):
        self.VI_M.estimate_vid(webcam_id, bpm, setup)

    def img_estimation(self, file, bpm=120):
        self.VI_M.estimate_img(file, bpm)


if __name__ == "__main__":
    app = Main()
    # app.live_estimation(webcam_id="http://10.30.54.36/live", setup=False)
    app.img_estimation('images/trial3.jpg', 240)
