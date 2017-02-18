#!/usr/bin/env python3
'''
    This sample program shows how to control a motor using a joystick. In the
    operator control part of the program, the joystick is read and the value
    is written to the motor.

    Joystick analog values range from -1 to 1 and speed controller inputs also
    range from -1 to 1 making it easy to work together. The program also delays
    a short time in the loop to allow other threads to run. This is generally
    a good idea, especially since the joystick values are only transmitted
    from the Driver Station once every 20ms.
'''

import wpilib
import logging
logging.basicConfig(level=logging.DEBUG)

s = 1.5


def curve(x):
    return pow(x, s) if x >= 0 else -pow(-x, s)


class MyRobot(wpilib.SampleRobot):

    #: update every 0.005 seconds/5 milliseconds (200Hz)
    kUpdatePeriod = 0.005

    def robotInit(self):
        '''Robot initialization function'''

        self.stick = wpilib.Joystick(0)
        self.rstick = wpilib.Joystick(1)

        self.motor_left = wpilib.Victor(0)
        self.motor_right = wpilib.Victor(1)
        self.motor_gobbler = wpilib.Victor(2)
        self.motor_shooter = wpilib.Victor(3)

        self.speed_gobbler = 0
        self.speed_shooter = 0

    def operatorControl(self):
        '''Runs the motor from a joystick.'''
        logging.info('op-control satrted')

        while self.isOperatorControl() and self.isEnabled():

            
            left = self.stick.getY()
            right = self.rstick.getY() #RawAxis(self.stick.axes[2])

            if self.stick.getRawButton(4) and self.speed_gobbler < 1:
                self.speed_gobbler += .005
            elif self.stick.getRawButton(1) and self.speed_gobbler > 0:
                self.speed_gobbler -= .005

                
            if self.stick.getRawButton(6) and self.speed_shooter < 1:
                self.speed_shooter += .005
            elif self.stick.getRawButton(5) and self.speed_shooter > 0:
                self.speed_shooter -= .005

            for i in range(5):
                logging.info('%d: %f' % (i, self.stick.getRawAxis(i)))

            if self.stick.getRawButton(2):
                gobbler = -.5
            else:
                gobbler = self.speed_gobbler
            
            r = curve(right) #max(min(x + y, 1.0), -1.0))
            l = curve(left) #max(min(y - x, 1.0), -1.0))
            
            self.motor_left.set(-l)
            self.motor_right.set(r)
            self.motor_gobbler.set(gobbler )
            self.motor_shooter.set(self.speed_shooter)
                                   
            wpilib.Timer.delay(self.kUpdatePeriod)  # wait 5ms to the next update


if __name__ == "__main__":
    wpilib.run(MyRobot)
