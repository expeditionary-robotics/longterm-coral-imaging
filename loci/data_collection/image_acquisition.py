"""Collects images from a Prosilica GC Allied Vision Camera.

Adapted from VimbaPython/Examples/asynchronous_grab_opencv.py
"""
import os
import argparse
from vimba import *

from loci.data_collection.utils import get_camera, setup_camera, FrameHandler


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Data acquisition and recording protocol.")
    parser.add_argument("-w", "--write_path", type=str, action="store", default=os.getenv("OUTPUT_DIR"), help="Provide a target to write files")
    parser.add_argument("-fps", "--frames_per_second", type=int, action="store", default=1, help="Frames per second to record (1, 2, 3 or 4)")
    parser.add_argument("-b", "--buffer", type=int, action="store", default=10, help="Number of frames to buffer when streaming.")
    parser.add_argument("-v", "--verbose", type=bool, action="store", default=False, help="Whether to print to screen or render images.")
    parser.add_argument("-xml", "--xml_settings", type=str, action="store", default="", help="Provide a target for user settings files" )
    parser.add_argument("-e", "--exposure", type=int, action="store", default=4000, help="Set absolute exposure time.")

    args = parser.parse_args()
    fps = args.frames_per_second
    write_path = args.write_path
    stream_buffer = args.buffer
    verbose = args.verbose
    settings_xml = args.xml_settings
    exposure_time = args.exposure

    # Make the write path target if it is not already in existence
    if os.path.exists(write_path) is False:
        os.makedirs(write_path)

    # Create the camera image acquisition
    with Vimba.get_instance():
        with get_camera(None) as cam:

            # Start streaming at the frame rate specified
            setup_camera(cam, fps=fps, exposure_time=exposure_time, settings_file=settings_xml)
            handler = FrameHandler(verbose=verbose, file_target=write_path)

            try:
                # Start Streaming with a custom a buffer of 10 Frames (defaults to 5)
                cam.start_streaming(handler=handler, buffer_count=stream_buffer, allocation_mode=AllocationMode.AnnounceFrame)
                handler.shutdown_event.wait()

            finally:
                cam.stop_streaming()
