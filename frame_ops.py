import os
import cv2 as cv
import numpy as np


# Contains operations to perform on an individual frame
class FrameOperations():

    def __init__(self):
        self.CWD = os.getcwd()
        self.RES_F = os.path.join(self.CWD, 'resources')
        self.FILTER_F = os.path.join(self.RES_F, 'FILTERS')
        self.SPEED_FILTER = cv.imread(os.path.join(self.FILTER_F, "SPEED.png"))
        self.CONT_FILTER = cv.imread(
            os.path.join(self.FILTER_F, "CONTINUE.png"))

    def order_points(pts):
        # Initialize a list of coordinates that will be ordered as followed:
        # top-left, top-right, bottom-right, bottom-left
        rect = np.zeros((4, 2), dtype="float32")

        # Top-left point will have smallest sum, bottom-right will have largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        # Compute the difference between the points:
        # top-right point will have smallest difference, bottom-left will have the largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def four_point_transform(image, pts):
        # Obtain a consistent order of the points and unpack them individually
        rect = order_points(pts)
        (tl, tr, br, bl) = rect
        # Compute the width of the new image: max distance btw b-right and b-left or the t-right and t-left x-coords
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        # Compute the height of the new image: max distance btw the t-right and b-right or t-left and b-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        # Construct set of destination points to obtain a top-down view of the image in order:
        # top-left, top-right, bottom-right, bottom-left
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")
        # Compute the perspective transform matrix and apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped

    def average_blur(self, frame, kernel_size):
        conversion = cv.blur(frame, kernel_size)
        return conversion

    def gauss_blur(self, frame, kernel_size, sigX):
        conversion = cv.GaussianBlur(frame, kernel_size, sigX)
        return conversion

    def convert_scale_abs(self, frame, alpha, beta):
        """alpha must be float, beta must be int!"""
        # alpha for contrast control, beta for brightness control

        conversion = cv.convertScaleAbs(frame, alpha=alpha, beta=beta)

        return conversion

    def contrast_brightness(self, frame, brightness, contrast):

        conversion = np.int16(frame)
        conversion = conversion * (contrast/127+1) - contrast + brightness
        conversion = np.clip(conversion, 0, 255)
        # unsigned int
        conversion = np.uint8(conversion)

        return conversion

    def clahe(self, frame):
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv.createCLAHE(clipLimit=3., tileGridSize=(8, 8))

        # convert from BGR to LAB color space
        lab = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
        l, a, b = cv.split(lab)  # split on 3 different channels

        l2 = clahe.apply(l)  # apply CLAHE to the L-channel

        lab = cv.merge((l2, a, b))  # merge channels
        # convert from LAB to BGR
        conversion = cv.cvtColor(lab, cv.COLOR_LAB2BGR)

        return conversion

    def increase_red(self, frame):
        B, G, R = cv.split(frame)
        B = self.contrast_brightness(B, 10, 10)
        G = self.contrast_brightness(G, 1, 1)
        R = self.contrast_brightness(R, 1000, 1000)

        # merge B,G,R
        higher_red = cv.merge([B, G, R])

        return higher_red

    def apply_filters(self, frame):
        frame_h, frame_w = frame.shape[:2]

        trans_mask = self.CONT_FILTER[:, :, 2] == 0
        self.CONT_FILTER[trans_mask] = [-1, -1, -1]

        self.CONT_FILTER = cv.resize(
            self.CONT_FILTER, (frame_w, frame_h), interpolation=cv.INTER_LINEAR)
        self.SPEED_FILTER = cv.resize(
            self.SPEED_FILTER, (frame_w, frame_h), interpolation=cv.INTER_LINEAR)

        filtered = cv.addWeighted(frame, 1, self.CONT_FILTER, 0.3, -15)
        filtered = cv.addWeighted(filtered, 0.7, self.SPEED_FILTER, 0.3, -15)

        return filtered

    def found_frame_operation(self, frame):
        """Performs all operations on the found frame
        Use if you want to test out multiple options"""

        frame = self.apply_filters(frame)

        return frame
