#!/usr/bin/env python3

import numpy as np
from time import time
from cscore import CameraServer
from networktables import NetworkTables

def main():

    # Get ready with default camera and enable cscore logginf
    cs = CameraServer.getInstance()
    cs.enableLogging()
    
    # Enable capturing (waiting for a streaming client to connect)
    camera0 = cs.startAutomaticCapture(dev=0, name='Jetson Camera 0')
    camera1 = cs.startAutomaticCapture(dev=1, name='Jetson Camera 1')
    # cs.startAutomaticCapture(dev=2, name='Jetson Camera 2')

    camera0.setResolution(160, 120)
    camera1.setResolution(160, 120)

    cvSink0 = cs.getVideo(camera=camera0)
    cvSink1 = cs.getVideo(camera=camera1)

    outputStream = cs.putVideo("Swappable", 160, 120)

    img = np.zeros(shape=(120, 160, 3), dtype=np.uint8)

    sd = NetworkTables.getTable("SmartDashboard/DB") 

    while True:
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

