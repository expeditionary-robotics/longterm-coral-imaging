"""Aligns GPS data with corresponding image pointers."""

import os
import pandas as pd
import argparse
import matplotlib.pyplot as plt



if __name__ == "__main__":
    # Parse command line info
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--image_files", type=str, action="store", default="./", help="Path to file containing images you would like to assign coordinates.")
    parser.add_argument("-p", "--poses", type=str, action="store", default=None, help="File which contains GPS data and times.")
    parser.add_argument("-m", "--interp_method", type=str, action="store", default="interpolate_gps",
                         help="Set method for inteprolating; choose closest (assigns nearest GPS pose in time to camera image) or interpolate_gps (guesses GPS coordinate)")

    args = parser.parse_args()

    image_target_path = args.image_files
    pose_target_file = args.poses
    interp_method = args.interp_method

    # Grab the image name
    fname_labels = []
    for fname in os.listdir(image_target_path):
        if "png" in fname:
            # Make sure that any copies are ignored, for simplicity
            fname_labels.append(fname)

    # Get image times
    image_times = [float(fn.split("_")[3])/1e9 for fn in fname_labels]

    # Create a pandas dataframe of the file names and times
    df = pd.DataFrame(dict(file_name=fname_labels, file_time=image_times))
    # df.loc[:, "human_readable_timestamp"] = pd.to_datetime(df.file_time, unit="s", utc=True)
    df.set_index("file_time", inplace=True)
    df.sort_index(axis=0, inplace=True)
    print(df)

    # Create a pandas dataframe of the GPS data
    ## ASSUMES CREATED USING PYMAVLINKDUMP
    pos_df = pd.read_csv(pose_target_file, header=0, dtype=float)
    pos_df["timestamp"] = pos_df.timestamp.values.astype(float)
    # pos_df.loc[:, "human_readable_timestamp"] = pd.to_datetime(pos_df.timestamp, unit="s", utc=True)
    pos_df.set_index("timestamp", inplace=True)
    pos_df.sort_index(axis=0, inplace=True)
    print(pos_df)

    # Merge the datasets 
    ind = df.index
    merged = pd.concat([df, pos_df], axis=1)
    print(merged)
    merged = merged.sort_index(axis=0)
    if interp_method == "closest":
        interpolated = merged.interpolate(method="nearest")
    else:
        interpolated = merged.interpolate(method="index")
    all_df = interpolated.loc[ind]
    print(all_df)

    # Save
    all_df.to_csv(f"./output/all_1207_trial2.csv")

    plt.plot(all_df.Lng, all_df.Lat)
    plt.show()
