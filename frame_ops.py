import os
import cv2 as cv
import numpy as np


# Contains operations to perform on an individual frame
class FrameOperations():

    def __init__(self):
        pass

    def order_points(self, pts):
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

    def four_point_transform(self, image, pts):
        """
        Parameters:
        - image: array containing grid
        - pts: array of 4 points from corners of grid
        Returns:
        - warped: birds-eye, top-down view of grid from image parameter 
        """
        # Obtain a consistent order of the points and unpack them individually
        rect = self.order_points(pts)
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
        M = cv.getPerspectiveTransform(rect, dst)
        warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped
