"""Takes array targets and converts to png images."""

import argparse
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description="Process image folder target for debug visualization",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file_target", type=str, default=os.path.join(os.getenv("OUTPUT_DIR"), "dockwater_test"), action="store", help="Path to image targets")
    parser.add_argument("-w", "--write_target", type=str, default="")
    parser.add_argument("-v", "--verbose", type=bool, default=False)

    # Get the user arguments
    args = parser.parse_args()
    target_path = args.file_target
    write_path = args.write_target
    verbose = args.verbose

    for fname in os.listdir(target_path):
        if ".npy" in fname:
            # convert to an image
            array_target = np.load(os.path.join(target_path, fname))
            img = cv2.cvtColor(array_target, cv2.COLOR_BAYER_GR2RGB)
            img = img*16
            # img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            # cropped_img = img[50:-50, 50:-50, :]
            if verbose is True:
                cv2.namedWindow("image", cv2.WINDOW_NORMAL)
                cv2.imshow("image", img)
                cv2.resizeWindow("image", 1000, 1000)
                cv2.waitKey(-1)
            else:
                pass

            if write_path != "":
                target_strip = fname.split(".")[0]
                filename = os.path.join(write_path, f"png_{target_strip}.png")
                cv2.imwrite(filename, img)

        else:
            print(f"No valid image at {fname}, skipping.")
            continue


if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()
