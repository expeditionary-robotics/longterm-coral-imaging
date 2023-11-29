"""Functions and classes to assist with data acquisition."""

import threading
import sys
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


def setup_camera(cam: Camera, fps: int=4):
    """Set consistent camera settings for image logging.
    
    TODO[vpreston] Check that these are the settings we want to use."""
    with cam:
        # Enable auto exposure time setting if camera supports it
        try:
            cam.ExposureAuto.set('Continuous')

        except (AttributeError, VimbaFeatureError):
            print("Cannot set exposure.")
            pass

        # Enable white balancing if camera supports it
        try:
            cam.BalanceWhiteAuto.set('Continuous')

        except (AttributeError, VimbaFeatureError):
            print("Cannot set white balance.")
            pass

        # Try to adjust Ge"Oops! Can't set that!")V packet size. This Feature is only available for GigE - Cameras.
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
        cam.set_pixel_format(cam_formats[2])  # set to maximum bit depth image for GC1380C


class FrameHandler:
    def __init__(self, verbose=False, display=False, write_to_file=True, write_path="./"):
        self.shutdown_event = threading.Event()
        self.verbose = verbose  # whether to print to terminal
        self.display = display  # whether to render image on a screen
        self.write_to_file = write_to_file  # whetehr to save the image to file


    def __call__(self, cam: Camera, frame: Frame):
        ENTER_KEY_CODE = 13

        key = cv2.waitKey(1)
        if key == ENTER_KEY_CODE:
            self.shutdown_event.set()
            return

        elif frame.get_status() == FrameStatus.Complete:
            capture_time = time.time_ns()  # time since epoch in seconds
            # print(frame.get_timestamp())
            # print(capture_time)
            if self.verbose:
                print('{} acquired {}'.format(cam, frame), flush=True)

            frame_data = frame.as_numpy_ndarray() # replaces the original vimba.Frame object with a numpy.ndarray
            frame_transport = cv2.cvtColor(frame_data, cv2.COLOR_BAYER_RG2RGB) # converts to an opencv color type that renders
            
            if self.write_to_file:
                np.save(f'array_{frame.get_id()}_{capture_time}', frame_data)
                cv2.imwrite(f'image_{frame.get_id()}_{capture_time}.png', frame_transport*16)  # saves a nicely rendered image to png format
                
            if self.display:
                msg = 'Stream from \'{}\'. Press <Enter> to stop stream.'
                cv2.imshow(msg.format(cam.get_name()), frame_transport*16)  # creates a nicely rendered image onscreen
            
        cam.queue_frame(frame)
