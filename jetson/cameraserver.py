#!/usr/bin/env python3

import numpy as np
from time import sleep
from cscore import CameraServer
from networktables import NetworkTables
from os import system

def main():

    # Get ready with default camera and enable cscore logginf
    cs = CameraServer.getInstance()
    cs.enableLogging()
 
    # Find usable cameras (those which support YUYV mode)
    camera_ids = []
    for id in range(3):
        if system('v4l2-ctl --all -d /dev/video%s | grep "Pixel Format" | grep RG10' % id) != 0:
            camera_ids.append(id)

    # Check that we found at least two usable cameras
    assert len(camera_ids) >= 2

    # Enable capturing (waiting for a streaming client to connect)
    camera0 = cs.startAutomaticCapture(dev=camera_ids[0], name='Jetson Camera 0')
    camera1 = cs.startAutomaticCapture(dev=camera_ids[1], name='Jetson Camera 1')
    # cs.startAutomaticCapture(dev=2, name='Jetson Camera 2')

    camera0.setResolution(160, 120)
    camera1.setResolution(160, 120)

    cvSink0 = cs.getVideo(camera=camera0)
    cvSink1 = cs.getVideo(camera=camera1)

    outputStream = cs.putVideo("Swappable", 160, 120)

    img = np.zeros(shape=(120, 160, 3), dtype=np.uint8)

    sd = NetworkTables.getTable("SmartDashboard/DB") 

    while True:

        # Allow Button 3 (from Dashboard) state change to exit,
        # thus forcing a restart
        if sd.getBoolean("Button 3", False):
            # wait a bit, then set button back to Off
            sleep(0.5)
            sd.putBoolean("Button 3", True)
            sleep(0.5)
            break

        # Allow Button 0 (from Dashboard) to select camera source
        if sd.getBoolean("Button 0", False):
            sink = cvSink0
        else:
            sink = cvSink1

        t, img = sink.grabFrame(img)
        if t == 0:
            outputStream.notifyError(sink.getError())
            continue

        outputStream.putFrame(img)
    
    
if __name__ == '__main__':
    
    # This allows debug level logging from all components
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Point networktables to the RoboRIO server
    NetworkTables.initialize(server='10.57.28.2')     

    main()

