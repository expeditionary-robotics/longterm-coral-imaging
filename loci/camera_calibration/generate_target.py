"""Generates a calibration target for camera intrinsics and extrinsics estimation."""

import os
import cv2
import matplotlib as mpl
import matplotlib.pyplot as plt

from cv2 import aruco

if __name__ == "__main__":
    workdir = "./output/"
    aruco_dict = aruco.Dictionary_get(aruco.DICT_APRILTAG_36h10)
    board = aruco.CharucoBoard_create(7, 5, 1.0, 0.8, aruco_dict)
    imboard = board.draw((2000, 2000))
    cv2.imwrite(workdir + "chessboard.tiff", imboard)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.imshow(imboard, cmap = mpl.cm.gray, interpolation = "nearest")
    ax.axis("off")
    plt.show()
