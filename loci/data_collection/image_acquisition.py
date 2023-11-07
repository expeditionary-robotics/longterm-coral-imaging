"""Collects images from a Prosilica GC Allied Vision Camera.

Adapted from VimbaPython/Examples/asynchronous_grab_opencv.py
"""
import os
import argparse
from vimba import *

from loci.data_collection.utils import get_camera, setup_camera, FrameHandler


if __name__ == '__main__':
    with Vimba.get_instance():
        with get_camera() as cam:

            # Start Streaming, wait for five seconds, stop streaming
            setup_camera(cam)
            handler = FrameHandler()

            try:
                # Start Streaming with a custom a buffer of 10 Frames (defaults to 5)
                cam.start_streaming(handler=handler, buffer_count=10)
                handler.shutdown_event.wait()

            finally:
                cam.stop_streaming()
