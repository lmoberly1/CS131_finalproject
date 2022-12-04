import cv2 as cv
from beatboard import Beatboard


class VideoManager():

    def __init__(self):
        self.BEATBOARD = Beatboard()  # piano
        self.board = None

    def get_board(self, frame):
        """
        Parameters:
        - frame: image of grid
        Function:
        - updates self.board with 2d int array of grid (int corresponds to shape in grid, 0 if empty)
        """
        print('GETTING BOARD')
        grid_rgb, grid_gray = self.BEATBOARD.detect_grid(
            frame)
        self.board = self.BEATBOARD.set_board(grid_gray)

    def estimate_img(self, image, bpm):
        """
        Parameters:
        - image: image of grid
        - bpm: beats per minute
        Function:
        - plays notes taken from shapes on grid
        """
        try:
            while True:
                frame = cv.imread(image)
                # Getting first board
                if self.board is None:
                    print("Getting initial board.")
                    self.get_board(frame)
                # Playing board
                self.BEATBOARD.play_board(
                    (self.board).T, self.get_board, bpm, frame=frame)
        except KeyboardInterrupt:
            print('End Program.')

    def estimate_vid(self, webcam_id, bpm, setup):
        """
        Parameters:
        - webcam_id: source of live video
        - bpm: beats per minute
        - setup: setup mode (only shows live video and doesn't play board)
        Function:
        - detects grid from frame every 8 beats
        - plays board for 8 beats
        """

        cap = cv.VideoCapture(webcam_id)
        cap.set(3, 1920)
        cap.set(4, 1080)

        # Setup mode: only shows live feed and doesn't play board
        if setup:
            print('IN SETUP MODE')
            try:
                while True:
                    # Show video
                    has_frame, frame = cap.read()
                    cv.imshow('Video Output', frame)
                    if cv.waitKey(1) & 0xFF == ord('q'):
                        break
            except KeyboardInterrupt:
                print('End Program.')

        # Live production mode
        else:
            try:
                frame_count = 0
                fps = 30
                save_interval = (60 / bpm) * 8
                print('FPS: ', fps)
                print('Time of 1 Measure (s): ', save_interval)

                # Infinite Play Loop
                while(True):
                    has_frame, frame = cap.read()
                    cv.imshow('Video Output', frame)
                    try:
                        # Getting first board
                        if self.board is None:
                            print("Getting initial board.")
                            self.get_board(frame)
                        # Playing board
                        self.BEATBOARD.play_board(
                            (self.board).T, self.get_board, bpm, frame=frame)
                    except Exception as e:
                        print('Exception: ', e)
                        break

            except KeyboardInterrupt:
                print('End Program.')
