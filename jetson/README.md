## Code used on the Jetson TX1

The actual script serving the camera streams is cameraserver.py.

The additional systemd service definition file can be used to
make the cameraserver to be a system service, so that it can
be auto-started, can do failure recovery, and even allow the
cameraserver.py to be restarted remotely from the FRC Dashboard
using "Button 3".

The remote restart is actually achieved in conjunction with the systemd
service script: activating Button 3 on the dashboard will make the
cameraserver.py loop to break and hence cameraserver.py to exit.
The systemd script will then attempt to restart the cameraserver (since
it detects that it has died). Note that while Button 3 is active, the
cameraserver.py process will keep exiting. So, in order to allow it to
properly run, Button 3 must be toggled back to "Off" position.

For the above to work, the cameraserver.service systemd file needs
to be copied into /lib/systemd/system and then enabled. The actual
steps:

```
sudo cp lib-systemd-system/cameraservice.service /lib/systemd/system
sudo chmod 644 /lib/systemd/system/cameraserver.service
sudo systemctl daemon-reload
sudo systemctl enable cameraserver.service
```

After reboot, the cameraserver.py will now be auto-started.

Some useful commands:

To show status of cameraserver, including the last many lines
of its log:

```
systemctl status cameraserver.service
```

To stop/start/restart cameraserver manually:

```
sudo systemctl stop cameraserver.service
sudo systemctl start cameraserver.service
sudo systemctl restart cameraserver.service
```
