import cv2 as cv
from frame_ops import FrameOperations
from distance_between import DistanceEstimator

class VideoManager():

    def __init__(self):
        self.DISTANCE_ESTIMATOR = DistanceEstimator()
        self.FRAME_OPS = FrameOperations()

        self.FIRST = True

    def estimate_vid(self, webcam_id=0):
        """
        Reads webcam, applies distance estimation on webcam
        """
        cap = cv.VideoCapture(webcam_id)

        while(True):
            has_frame, frame = cap.read()

            if self.FIRST:
                self.WEB_CAM_H, self.WEB_CAM_W = frame.shape[0:2]
                self.FIRST = False

            frame = self.DISTANCE_ESTIMATOR.get_distance(frame)
            cv.imshow('frame', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

