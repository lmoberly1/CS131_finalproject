from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2 as cv


class DistanceEstimator():

    def __init__(self):

        self.REF_WIDTH = 3

    def midpoint(self, ptA, ptB):
        return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

    def get_distance(self, frame):
        frame_h, frame_w = frame.shape[0:2]

        # Convert to grayscale and perform Gaussian Blur
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (7, 7), 0)

        # Perform Canny Edge Detection with dilation and erosion
        edged = cv.Canny(gray, 50, 100)
        edged = cv.dilate(edged, None, iterations=1)
        edged = cv.erode(edged, None, iterations=1)

        # Find contours in the edge map
        cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL,
                               cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if not cnts:
            print('no contours')
            return frame

        # Sort the contours from left-to-right; initialize the distance colors and reference object
        (cnts, _) = contours.sort_contours(cnts)
        colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255),
                  (255, 255, 0), (255, 0, 255))
        refObj = None

        # Loop over the contours individually
        orig = frame
        for c in cnts:
            # Ignore small contours
            if cv.contourArea(c) < 100:
                continue
            # Compute the rotated bounding box of the contour
            box = cv.minAreaRect(c)
            box = cv.cv.BoxPoints(
                box) if imutils.is_cv() else cv.boxPoints(box)
            box = np.array(box, dtype="int")

            # Order the points in the contour such that they appear in order:
            # top-left, top-right, bottom-right, and bottom-left
            box = perspective.order_points(box)
            # Compute the center of the bounding box
            cX = np.average(box[:, 0])
            cY = np.average(box[:, 1])

            # Set reference object if first contour
            if refObj is None:
                # Unpack the ordered bounding box and compute midpoint
                # between top-left and top-right points AND between the top-right and bottom-right
                (tl, tr, br, bl) = box
                (tlblX, tlblY) = self.midpoint(tl, bl)
                (trbrX, trbrY) = self.midpoint(tr, br)
                # Compute the Euclidean distance between the midpoints and construct the reference object
                D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                refObj = (box, (cX, cY), D / self.REF_WIDTH)
                continue

            # Draw the contours on the image
            orig = frame.copy()
            cv.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
            cv.drawContours(
                orig, [refObj[0].astype("int")], -1, (0, 255, 0), 2)
            # Stack the reference coordinates and the object coordinates to include the object center
            refCoords = np.vstack([refObj[0], refObj[1]])
            objCoords = np.vstack([box, (cX, cY)])

            i = 0
            # Loop over the original points
            for ((xA, yA), (xB, yB), color) in zip(refCoords, objCoords, colors):
                if i != 4:  # only get midpoint
                    i += 1
                    continue
                # Draw circles corresponding to the current points and connect them with a line
                cv.circle(orig, (int(xA), int(yA)), 5, color, -1)
                cv.circle(orig, (int(xB), int(yB)), 5, color, -1)
                cv.line(orig, (int(xA), int(yA)), (int(xB), int(yB)),
                        color, 2)
                # Compute the Euclidean distance between the coords and
                # convert the distance in pixels to distance in units
                D = dist.euclidean((xA, yA), (xB, yB)) / refObj[2]
                (mX, mY) = self.midpoint((xA, yA), (xB, yB))
                cv.putText(orig, "{:.1f}in".format(D), (int(mX), int(mY - 10)),
                           cv.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
                # show the output image
                # cv.imshow("Image", orig)
                # cv.waitKey(0)
                i += 1

        return orig


"""
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
ap.add_argument("-w", "--width", type=float, required=True,
	help="width of the left-most object in the image (in inches)")
args = vars(ap.parse_args())

# load the image, convert it to grayscale, and blur it slightly
image = cv.imread(args["image"])
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
gray = cv.GaussianBlur(gray, (7, 7), 0)
# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv.Canny(gray, 50, 100)
edged = cv.dilate(edged, None, iterations=1)
edged = cv.erode(edged, None, iterations=1)
# find contours in the edge map
cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL,
	cv.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
# sort the contours from left-to-right and, then initialize the
# distance colors and reference object
(cnts, _) = contours.sort_contours(cnts)
colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255), (255, 255, 0),
	(255, 0, 255))
refObj = None

# loop over the contours individually
for c in cnts:
	# if the contour is not sufficiently large, ignore it
	if cv.contourArea(c) < 100:
		continue
	# compute the rotated bounding box of the contour
	box = cv.minAreaRect(c)
	box = cv.cv.BoxPoints(box) if imutils.is_cv() else cv.boxPoints(box)
	box = np.array(box, dtype="int")
	# order the points in the contour such that they appear
	# in top-left, top-right, bottom-right, and bottom-left
	# order, then draw the outline of the rotated bounding
	# box
	box = perspective.order_points(box)
	# compute the center of the bounding box
	cX = np.average(box[:, 0])
	cY = np.average(box[:, 1])

  # if this is the first contour we are examining (i.e.,
	# the left-most contour), we presume this is the
	# reference object
	if refObj is None:
		# unpack the ordered bounding box, then compute the
		# midpoint between the top-left and top-right points,
		# followed by the midpoint between the top-right and
		# bottom-right
		(tl, tr, br, bl) = box
		(tlblX, tlblY) = midpoint(tl, bl)
		(trbrX, trbrY) = midpoint(tr, br)
		# compute the Euclidean distance between the midpoints,
		# then construct the reference object
		D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
		refObj = (box, (cX, cY), D / args["width"])
		continue

  # draw the contours on the image
	orig = image.copy()
	cv.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
	cv.drawContours(orig, [refObj[0].astype("int")], -1, (0, 255, 0), 2)
	# stack the reference coordinates and the object coordinates
	# to include the object center
	refCoords = np.vstack([refObj[0], refObj[1]])
	objCoords = np.vstack([box, (cX, cY)])

  # loop over the original points
	for ((xA, yA), (xB, yB), color) in zip(refCoords, objCoords, colors):
		# draw circles corresponding to the current points and
		# connect them with a line
		cv.circle(orig, (int(xA), int(yA)), 5, color, -1)
		cv.circle(orig, (int(xB), int(yB)), 5, color, -1)
		cv.line(orig, (int(xA), int(yA)), (int(xB), int(yB)),
			color, 2)
		# compute the Euclidean distance between the coordinates,
		# and then convert the distance in pixels to distance in
		# units
		D = dist.euclidean((xA, yA), (xB, yB)) / refObj[2]
		(mX, mY) = midpoint((xA, yA), (xB, yB))
		cv.putText(orig, "{:.1f}in".format(D), (int(mX), int(mY - 10)),
			cv.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
		# show the output image
		cv.imshow("Image", orig)
		cv.waitKey(0)
"""
