from cscore import CameraServer

def main():

    # Get ready with default camera and enable cscore logginf
    cs = CameraServer.getInstance()
    cs.enableLogging()
    
    # Enable capturing (waiting for a streaming client to connect)
    cs.startAutomaticCapture(dev=0, name='Jetson Camera 1')
    cs.startAutomaticCapture(dev=2, name='Jetson Camera 2')
    cs.waitForever()
    
    
if __name__ == '__main__':
    
    # This allows debug level logging from all components
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Point networktables to the RoboRIO server
    from networktables import NetworkTables
    NetworkTables.initialize(server='10.57.28.2')     

    main()

