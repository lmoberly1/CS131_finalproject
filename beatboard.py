from skimage.segmentation import clear_border
import cv2 as cv
import pygame as pg
import numpy as np
import imutils
from frame_ops import FrameOperations
from sound_ops import SoundOperations
from time import sleep
import threading


class Beatboard():

    def __init__(self):
        self.FRAME_OPS = FrameOperations()
        self.SOUND_OPS = SoundOperations()
        self.frequencies = [523, 494, 440, 392, 349, 330, 294, 263]  # C5 to C4

    def extract_shape(self, cell):
        """
        Parameters:
        - cell: image of individual cell (possibly with shape)
        Returns:
        - num_edges: number of edges if shape, else None
        """
        # Thresholding and clearing any connected borders
        thresh = cv.threshold(cell, 0, 255,
                              cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
        thresh = clear_border(thresh)

        # Find contours in the thresholded cell
        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,
                               cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # if no contours were found than this is an empty cell
        if len(cnts) == 0:
            return None
        else:
            cv.imwrite('images/trial5_cell.jpg', thresh)
            return 1
            # i = 0
            # for contour in cnts:
            #     # Approximate the shape
            #     approx = cv.approxPolyDP(
            #         contour, 0.01 * cv.arcLength(contour, True), True)

            #     # Putting shape name at center of each shape
            #     if len(approx) == 3:
            #         return 3
            #     elif len(approx) == 4:
            #         return 4
            #     elif len(approx) == 5:
            #         return 5
            #     elif len(approx) == 6:
            #         return 6
            #     else:
            #         return 1

    def detect_grid(self, img):
        """
        Parameters:
        - img: image containing grid
        Returns:
        - 2-tuple of grid in both RGB and grayscale
        """

        # Grayscale and Gaussian Blur
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        cv.imwrite('images/trial5_gray.jpg', img_gray)
        img_blur = cv.GaussianBlur(img_gray, (3, 3), 0)
        cv.imwrite('images/trial5_blur.jpg', img_blur)

        # Canny Edge Detection
        # edges = cv.Canny(image=img_blur, threshold1=100,
        #                  threshold2=200)

        # Adaptive Thresholding
        thresh = cv.adaptiveThreshold(img_blur, 255,
                                      cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
        if thresh is None:
            raise Exception(
                ("Could not threshold object."))
        thresh = cv.bitwise_not(thresh)
        cv.imwrite('images/trial5_thresh.jpg', thresh)

        # Contour Detection
        contours, _ = cv.findContours(
            thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        contours = sorted(contours, key=cv.contourArea, reverse=True)

        # Find Grid Outline
        gridOutline = None
        # Loop over the contours
        for c in contours:
            # Approximate the contour
            peri = cv.arcLength(c, True)
            approx = cv.approxPolyDP(c, 0.02 * peri, True)
            # If contour has 4 points, assume we have found grid outline
            if len(approx) == 4:
                gridOutline = approx
                break

        if gridOutline is None:
            raise Exception(
                ("Could not find grid outline. Debug thresholding and contour steps."))

        grid = self.FRAME_OPS.four_point_transform(
            img, gridOutline.reshape(4, 2))
        gray_grid = self.FRAME_OPS.four_point_transform(
            img_gray, gridOutline.reshape(4, 2))
        cv.imwrite('images/trial5_transform.jpg', gray_grid)

        return (grid, gray_grid)

    def set_board(self, img):
        """
        Parameters:
        - img: image containing grid
        Returns:
        - board: 2d int array of grid (int corresponds to shape in grid, 0 if empty) 
        """

        # Initialize music grid
        board = np.zeros((8, 8), dtype="int")
        stepX = img.shape[1] // 8
        stepY = img.shape[0] // 8

        # Loop over the grid locations
        num_shapes = 0
        for y in range(0, 8):
            # Initialize the current list of cell locations
            row = []
            for x in range(0, 8):
                # Compute the starting and ending (x, y)-coordinates of the current cell
                startX = x * stepX
                startY = y * stepY
                endX = (x + 1) * stepX
                endY = (y + 1) * stepY
                # Add the (x, y)-coordinates to our cell locations list
                row.append((startX, startY, endX, endY))

                # Crop the cell from the warped transform image and then check for shape in the cell
                cell = img[startY:endY, startX:endX]
                shape = self.extract_shape(cell)
                # verify that the cell is not empty
                if shape is not None:
                    board[y, x] = shape
                    num_shapes += 1
        # Return board
        return board

    def play_board(self, board, get_new_board, bpm=60, frame=None):
        """
        Parameters:
        - board: 2d array, each row is one beat
        - get_new_board: callback function to update board
        - bpm: beats per minute
        - frame: new frame to pass into callback function
        Function:
        - loops through all 8 measures and plays sounds
        """
        sound_length = 60 / bpm
        double_board = np.append(board, board, axis=0)
        for j in range(16):
            # Get new board using callback function
            if j == 2:
                callback_thread = threading.Thread(
                    target=get_new_board, name="BoardUpdater", args=[frame])
                callback_thread.start()
            instruments = double_board[j]

            # If instrument, then play sound
            if np.count_nonzero(instruments) > 0:
                # Instruments has different values based on shape/instrument
                self.SOUND_OPS.play_sounds(
                    instruments, sound_length)
            sleep(sound_length)
