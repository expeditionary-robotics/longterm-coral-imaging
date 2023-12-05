"""Takes array targets and converts to png images with color correction."""

import argparse
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description="Process image folder target for debug visualization",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file_target", type=str, default=os.path.join(os.getenv("OUTPUT_DIR"), "dockwater_test"), action="store", help="Path to image targets")

    # Get the user arguments
    args = parser.parse_args()
    target_path = args.file_target

    summer = np.zeros((2048, 2048, 3))
    std_summer = np.zeros((2048, 2048, 3))
    count = 0

    # Compute average frame
    for fname in os.listdir(target_path):
        if ".npy" in fname:
            # convert to an image
            array_target = np.load(os.path.join(target_path, fname))
            img = cv2.cvtColor(array_target, cv2.COLOR_BAYER_GR2RGB)
            summer += img
            count += 1
        else:
            continue
    f_avg = summer / count

    # # Compute stdev frame
    # for fname in os.listdir(target_path):
    #     if ".npy" in fname:
    #         # convert to an image
    #         array_target = np.load(os.path.join(target_path, fname))
    #         img = cv2.cvtColor(array_target, cv2.COLOR_BAYER_GR2RGB)
    #         std_summer += (img - f_avg) ** 2
    #     else:
    #         continue
    # f_std = np.sqrt(std_summer / (count - 1))

    # Adjust image
    for fname in os.listdir(target_path):
        if ".npy" in fname:
            # convert to an image
            array_target = np.load(os.path.join(target_path, fname))
            img = cv2.cvtColor(array_target, cv2.COLOR_BAYER_GR2RGB)
            rbar = img / f_avg
            # sigmabar = np.mean(np.mean(f_std / f_avg, axis=0), axis=0)
            exp_convolve = cv2.filter2D(src=img, ddepth=-1, kernel=np.ones((7,7), np.float32))
            std_convolve = np.linalg.norm(img - exp_convolve, ord=1, axis=1)
            std_c = np.median(cv2.filter2D(src=std_convolve, ddepth=-1, kernel=np.ones((7,7), np.float32)) / exp_convolve)
            img = rbar * std_c
            img = cv2.normalize(img, None,  0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            cv2.namedWindow("image", cv2.WINDOW_NORMAL)
            cv2.imshow("image", img)
            cv2.resizeWindow("image", 1000, 1000)
            cv2.waitKey(-1)
        else:
            continue

if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()
