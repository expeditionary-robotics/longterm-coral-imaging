"""Uses OpenCV and a checkerboard target to calibrate camera parameters.

For this camera, leave it stationary, and move the target around. Make sure that
images that are captured by the camera contain the entire checkerboard. Vary location
in the frame, angle of the checkerboard, and distance from the camera during the process.

The calibrated parameters can then be fed into localization schema or post-processing software.

usage:
    flat_checkerboard_calibration.py [-f <image_folder_target>] [-w <width_cols>] [-r <height_rows>]
    [-s <square_size>] [-v <verbose_show_image>]

default values:
    ${OUTPUT_DIR}/calib_images for image targets
    11 cols
    8 rows
    20 square size
    verbose (show image) false

"""

import argparse
import os
import yaml
import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from cv2 import aruco


def main():
    parser = argparse.ArgumentParser(description="Process image folder target for calibration",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file_target", type=str, default=os.path.join(os.getenv("OUTPUT_DIR"), "calib_images"), action="store", help="Path to image targets")
    parser.add_argument("-w", "--width_cols", type=int, default=11, action="store", help="Number of columns on Charuco board")
    parser.add_argument("-r", "--height_rows", type=int, default=8, action="store", help="Number of rows on Charuco board")
    parser.add_argument("-s", "--square_size", type=float, default=20., action="store", help="Square size in [units] on board")
    parser.add_argument("-v", "--verbose", type=bool, action="store", default=False, help="Whether to render images to screen.")


    # Get the user arguments
    args = parser.parse_args()
    
    target_path = args.file_target
    cols = args.width_cols
    rows = args.height_rows 
    square_size = args.square_size 
    verbose = args.verbose

    # Set up the board object and detector
    board_size = (cols, rows)
    objp = np.zeros((board_size[0] * board_size[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)
    objp = objp * square_size
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Parse images in the target folder
    all_objs = []
    all_pts = []
    fnames = []
    fpaths = os.listdir(target_path)
    imgs_to_process = np.random.choice(fpaths, 50, replace=False)
    for fname in imgs_to_process:
        if ".npy" in fname:
            # convert to an image
            array_target = np.load(os.path.join(target_path, fname))
            frame_transport = cv2.cvtColor(array_target, cv2.COLOR_BAYER_GR2RGB) # converts to an opencv color type that renders
            img = cv2.normalize(frame_transport, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        else:
            img = None
        if img is None:
            print(f"No valid image at {fname}, skipping.")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, board_size, None)#, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        if ret is not True:
            print(f"No board found in image {fname}, skipping.")
            continue
        else:
            print(f"Board found in image {fname}!")
        
        fnames.append(fname)  # keep a record of the exact files, and order, processed
        all_objs.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        all_pts.append(corners2)

        # Show these steps for each image if verbose output wanted
        if verbose is True:
            detections = cv2.drawChessboardCorners(img.copy(), board_size, corners2, ret)
            cv2.imshow("Original Image", img)
            cv2.waitKey(0)
            cv2.imshow("Grayscale Image", gray)
            cv2.waitKey(0)
            cv2.imshow("Detections", detections)
            cv2.waitKey(0)
    
    # Calibrate
    rms, K, dist_coeffs, rvecs, tvecs, stdev_intr, stdev_extr, view_errors = cv2.calibrateCameraExtended(all_objs, all_pts, gray.shape[::-1], None, None)
    print(f"RMS: {rms}")
    print(f"Camera Matrix: {K}")
    print(f"Distortion Coeffs: {dist_coeffs.ravel()}")

    mean_error = 0
    for i in range(len(all_objs)):
        imgpoints2, _ = cv2.projectPoints(all_objs[i], rvecs[i], tvecs[i], K, dist_coeffs)
        error = cv2.norm(all_pts[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
    print( "total error: {}".format(mean_error/len(all_objs)))

    # Save the Calibration
    data = {'camera_matrix': np.asarray(K).tolist(),
            'dist_coeff': np.asarray(dist_coeffs).tolist(),
            'rms': np.asarray(rms).tolist(),
            'rvecs': np.asarray(rvecs).tolist(),
            'tvecs': np.asarray(tvecs).tolist(),
            'stdev_intrinsics': np.asarray(stdev_intr).tolist(),
            'stdev_extrinsics': np.asarray(stdev_extr).tolist(),
            'view_errors': np.asarray(view_errors).tolist(),
            'calibration_images': fnames}
    
    write_target = os.path.join(target_path, "calibration_matrix.yaml")
    with open(write_target, "w") as f:
        yaml.dump(data, f)
    print(f"Calibration information written to {write_target}.")

    # Show the results of undistortion is verbose output wanted
    if verbose is True:
        h, w = gray.shape[:2]
        newmat, roi = cv2.getOptimalNewCameraMatrix(K, dist_coeffs, (w, h), 1, (w, h))
        dst = cv2.undistort(gray.copy(), K, dist_coeffs, None, newmat)
        x, y, wr, hr = roi
        dst = dst[y:y+hr, x:x+wr]
        cv2.imshow("Original Image", gray)
        cv2.waitKey(0)
        cv2.imshow("Undistort Result", dst)
        cv2.waitKey(0)



if __name__ == "__main__":
    print(__doc__)
    main()
    cv2.destroyAllWindows()
