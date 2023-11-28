"""Uses OpenCV and a checkerboard target to calibrate camera parameters.

For this camera, leave it stationary, and move the target around. Make sure that
images that are captured by the camera contain the entire checkerboard. Vary location
in the frame, angle of the checkerboard, and distance from the camera during the process.

The calibrated parameters can then be fed into localization schema or post-processing software.
"""

import argparse
import cv2
from loci.data_collection.utils import FrameHandler

