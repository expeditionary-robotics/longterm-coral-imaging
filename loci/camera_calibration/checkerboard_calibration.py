"""Uses OpenCV and a checkerboard target to calibrate camera parameters.

For this camera, leave it stationary, and move the target around. Make sure that
images that are captured by the camera contain the entire checkerboard. Vary location
in the frame, angle of the checkerboard, and distance from the camera during the process.

The calibrated parameters can then be fed into localization schema or post-processing software.
"""

import argparse
import os
import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from cv2 import aruco

COLS = 11
ROWS = 8
SQUARE_SIZE = 20
MARKER_SIZE = 15

ARUCO_DICT = aruco.getPredefinedDictionary(aruco.DICT_7X7_1000)
BOARD = aruco.CharucoBoard((COLS, ROWS), SQUARE_SIZE, MARKER_SIZE, ARUCO_DICT)
BOARD.setLegacyPattern(True)
BOARD_IM = BOARD.generateImage((COLS*SQUARE_SIZE, ROWS*SQUARE_SIZE))

# plt.imshow(BOARD_IM)
# plt.show()

CPARAMS = aruco.CharucoParameters()
CPARAMS.tryRefineMarkers = True
DPARAMS = aruco.DetectorParameters()
RPARAMS = aruco.RefineParameters()


if __name__ == "__main__":
    # Read in the images that were saved to file
    print(os.getenv("OUTPUT_DIR"))
    image_loc = os.path.join(os.getenv("OUTPUT_DIR"), "calib_images")
    images = []
    for fname in os.listdir(image_loc):
        img = cv2.imread(os.path.join(image_loc, fname))
        if img is not None:
            images.append(img)
    
    all_corners = []
    all_ids = []
    all_objs = []
    all_pts = []
    for im in images:
        # Convert to grayscale
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        # plt.imshow(gray, cmap=mpl.cm.gray, interpolation="nearest")
        # plt.show()

        # Detect markers
        detector = aruco.CharucoDetector(BOARD, CPARAMS, DPARAMS, RPARAMS)
        corners, ids, _, _ = detector.detectBoard(gray)
        all_corners.append(corners)
        all_ids.append(ids)
        detections = aruco.drawDetectedCornersCharuco(im.copy(), corners, ids)
        # plt.imshow(detections)
        # plt.show()

        # Detect aruco symbols
        obj_pts, img_pts = BOARD.matchImagePoints(corners, ids)
        all_objs.append(obj_pts)
        all_pts.append(img_pts)

    
    # Calibrate
    (ret, camera_matrix, distortion_coeffs, \
     rvec, tvec, std_intrinsics, std_extrinsics, \
     perViewErrors) = cv2.calibrateCameraExtended(all_objs, all_pts, gray.shape[::-1], None, None)

    print(camera_matrix)
    print(distortion_coeffs)
    print(std_intrinsics)
    
    h, w = gray.shape[:2]
    newmat, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coeffs, (w, h), 1, (w, h))
    dst = cv2.undistort(gray.copy(), camera_matrix, distortion_coeffs, None, newmat)
    x, y, wr, hr = roi
    dst = dst[y:y+hr, x:x+wr]
    gscale = cv2.resize(gray, (int(hr/10), int(wr/10)))
    dscale = cv2.resize(dst, (int(hr/10), int(wr/10)))
    cv2.imshow("original", gscale)
    cv2.imshow("calibration result", dscale)
    cv2.waitKey(0)


    
