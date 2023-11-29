"""Aligns GPS data with corresponding image pointers."""

import os
import pandas as pd

# Choose whether to assign GPS coordinates to images using [closest] matching 
# timestamp, or an [interpolate_gps] procedure that fixes camera times
INTERP_METHOD = "closest"

if __name__ == "__main__":
    # Read in the names of the camera images, which contain timestamp information
    # Extract timestamp information from images
    # Read in the GPS data file
    # Extract timestamp information from data
    # Interpolate over camera and GPS timestamps; use camera timestamps as absolute basis
    # Create CSV with image name pointers and corresponding camera poses
    pass