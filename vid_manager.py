import cv2 as cv
from frame_ops import FrameOperations
from trombone import Trombone
from beatboard import Beatboard


class VideoManager():

    def __init__(self):
        self.TROMBONE = Trombone()  # trombone
        self.BEATBOARD = Beatboard()  # piano
        self.FRAME_OPS = FrameOperations()
        self.FIRST = True
        self.board = None

    def estimate_img(self):

        img = cv.imread('images/trial3.jpg')
        grid_rgb, grid_gray = self.BEATBOARD.detect_grid(img)
        board = self.BEATBOARD.set_board(grid_gray)

        self.BEATBOARD.play_board(board.T, 120)

    def get_board(self):
        # grid_rgb, grid_gray = self.BEATBOARD.detect_grid(
        #     frame)
        print('getting board')
        img = cv.imread('images/trial3.jpg')
        grid_rgb, grid_gray = self.BEATBOARD.detect_grid(
            img)
        self.board = self.BEATBOARD.set_board(grid_gray)

    def estimate_vid(self, webcam_id, bpm, program):

        cap = cv.VideoCapture(webcam_id)
        cap.set(3, 1920)
        cap.set(4, 1080)

        try:
            frame_count = 0
            fps = 30
            save_interval = (60 / bpm) * 8
            print('fps: ', fps)
            print('save: ', save_interval)
            while(True):
                has_frame, frame = cap.read()

                # Play music program
                if program == "trombone":
                    frame = self.TROMBONE.detect(frame)
                else:
                    print('NEW LOOP BITCHES')
                    try:
                        if self.board is None:
                            print("getting initial board")
                            self.get_board()
                        self.BEATBOARD.play_board(
                            (self.board).T, self.get_board, bpm)
                    except Exception as e:
                        print('Exception: ', e)
                        continue

                # Show video
                cv.imshow('Video Output', frame)

                if cv.waitKey(1) & 0xFF == ord('q'):
                    break

        except KeyboardInterrupt:
            print('End Program.')


# bpm = 120
# timetoplayboard_seconds = (60 / bpm) * 8

# after 6th beat, send back signal to take snapshot, process, and update board
