"""Generates a calibration target for camera intrinsics and extrinsics estimation.

Note: works only for opencv 4.8 and python 3.7+."""

import os
import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from cv2 import aruco

if __name__ == "__main__":
    workdir = "./output/"
    imboard = cv2.Mat(np.zeros((2000, 2000)))
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_36h10)
    ids = np.array([1, 2, 3])
    board = aruco.CharucoBoard((10, 8), 1, 0.8, aruco_dict)
    imboard = board.generateImage((2000, 2000), imboard, 10, 1)
    cv2.imwrite(workdir + "chessboard.tiff", imboard)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.imshow(imboard, cmap = mpl.cm.gray, interpolation = "nearest")
    ax.axis("off")
    plt.show()
