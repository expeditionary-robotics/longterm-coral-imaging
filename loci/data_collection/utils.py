"""Functions and classes to assist with data acquisition."""

import threading
import sys
import os
import cv2
import time
import numpy as np
from typing import Optional
from vimba import *


##############
# Image Capture Helpers
##############


def abort(reason: str, return_code: int = 1):
    """Automatic clean abort procedure."""
    print(reason + '\n')
    sys.exit(return_code)


def get_camera(camera_id: Optional[str]) -> Camera:
    """Access the target camera."""
    with Vimba.get_instance() as vimba:
        if camera_id:
            try:
                return vimba.get_camera_by_id(camera_id)

            except VimbaCameraError:
                abort('Failed to access Camera \'{}\'. Abort.'.format(camera_id))

        else:
            cams = vimba.get_all_cameras()
            if not cams:
                abort('No Cameras accessible. Abort.')

            return cams[0]


def setup_camera(cam: Camera, fps: int=4, exposure_time: int=4000, gain_setting: int=20, settings_file: str=""):
    """Set consistent camera settings for image logging."""
    with cam:
        # Load in saved user settings
        if settings_file != "":
            try:
                cam.load_settings(settings_file, PersistType.All)
            except (AttributeError, VimbaFeatureError):
                print(f"Cannot load settings from file {settings_file}")
                pass
        else:
            pass
        
        # Set auto exposure parameters
        try:
            feature = cam.get_feature_by_name("ExposureAutoMax")
            feature.set(exposure_time) #sets hard limit on exposure auto maximum value
            cam.ExposureAuto.set('Continuous')
        except (AttributeError, VimbaFeatureError):
            print("Cannot set exposure.")
            pass

        # Disable gain setting so that auto exposure works
        try:
            cam.GainAuto.set('Off')
            feature = cam.get_feature_by_name("GainRaw")
            feature.set(gain_setting)
        except (AttributeError, VimbaFeatureError):
            print("Cannot set gain.")
            pass

        # Disable white balancing
        try:
            cam.BalanceWhiteAuto.set('Off')
        except (AttributeError, VimbaFeatureError):
            print("Cannot set white balance.")
            pass

        # Try to adjust GeV packet size. This Feature is only available for GigE - Cameras.
        try:
            cam.GVSPAdjustPacketSize.run()
            while not cam.GVSPAdjustPacketSize.is_done():
                pass
        except (AttributeError, VimbaFeatureError):
            print("Cannot adjust packets.")
            pass
        
        # Enable specified frame rate for grabbing images
        try:
            feature = cam.get_feature_by_name("AcquisitionFrameRateAbs")
            feature.set(fps) #specifies 1FPS
            feature = cam.get_feature_by_name("TriggerSelector")
            feature.set("FrameStart")
            feature = cam.get_feature_by_name("TriggerMode")
            feature.set("Off")

        except (AttributeError, VimbaFeatureError):
            print("Cannot set frame rate.")
            pass

        # Select the pixel formatting
        cam_formats = cam.get_pixel_formats()
        print(cam_formats)
        cam.set_pixel_format(cam_formats[2])  # set to maximum bit depth image for GC1380C


class FrameHandler:
    def __init__(self, verbose=False, file_target="./"):
        self.shutdown_event = threading.Event()
        self.verbose = verbose  # whether to print to terminal or render images
        self.file_target = file_target  # where to write images to file


    def __call__(self, cam: Camera, frame: Frame):
        ENTER_KEY_CODE = 13

        key = cv2.waitKey(1)
        if key == ENTER_KEY_CODE:
            self.shutdown_event.set()
            return

        elif frame.get_status() == FrameStatus.Complete:
            capture_time = time.time_ns()  # time since epoch in seconds
            frame_time = frame.get_timestamp()

            # feature = cam.get_feature_by_name("ExposureTimeAbs")
            # print(feature)

            if self.verbose is True:
                print('{} acquired {} at {} with cam time {}'.format(cam, frame, capture_time, frame_time), flush=True)

            frame_data = frame.as_numpy_ndarray() # replaces the original vimba.Frame object with a numpy.ndarray    
            np.save(os.path.join(self.file_target, f'array_{frame.get_id()}_{capture_time}_{frame_time}'), frame_data)

            if self.verbose is True:
                frame_transport = cv2.cvtColor(frame_data, cv2.COLOR_BAYER_GR2RGB) # converts to an opencv color type that renders
                # frame_transport = cv2.cvtColor(frame_data, cv2.COLOR_BAYER_RG2RGB) # converts to an opencv color type that renders
                cv2.imwrite(os.path.join(self.file_target, f'pngimage_{frame.get_id()}_{capture_time}_{frame_time}.png'), frame_transport*16)
                msg = 'Stream from \'{}\'. Press <Enter> to stop stream.'
                cv2.imshow(msg.format(cam.get_name()), frame_transport*16)  # creates a nicely rendered image onscreen
            
        cam.queue_frame(frame)
