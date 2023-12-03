"""Takes array targets and converts to png images."""

import argparse
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description="Process image folder target for debug visualization",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file_target", type=str, default=os.path.join(os.getenv("OUTPUT_DIR"), "calib_images"), action="store", help="Path to image targets")

    # Get the user arguments
    args = parser.parse_args()
    target_path = args.file_target

    for fname in os.listdir(target_path):
        if ".npy" in fname:
            # convert to an image
            array_target = np.load(os.path.join(target_path, fname))
            img = cv2.cvtColor(array_target, cv2.COLOR_BAYER_GR2RGB) # converts to an opencv color type that renders
            cropped_img = img[50:-50, 50:-50, :]
            cv2.namedWindow("image", cv2.WINDOW_NORMAL)
            cv2.imshow("image", cropped_img*16)
            cv2.resizeWindow("image", 500, 500)
            cv2.waitKey(-1)
        else:
            img = None
        if img is None:
            print(f"No valid image at {fname}, skipping.")
            continue

if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()
