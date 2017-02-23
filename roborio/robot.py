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

import sys
import wpilib
import logging
from time import time

logging.basicConfig(level=logging.DEBUG)

s = 1.5


def curve(x):
    return pow(x, s) if x >= 0 else -pow(-x, s)


class MyRobot(wpilib.SampleRobot):

    #: update every 0.005 seconds/5 milliseconds (200Hz)
    kUpdatePeriod = 0.005

    def robotInit(self):
        '''Robot initialization function'''

        # code to show a camera
        wpilib.CameraServer.launch()

        self.stick = wpilib.Joystick(0)

        # below is the wheel controls controller 3 and 4
        self.motor_left = wpilib.Victor(0)
        
        # below is the wheel controls controller 1 and 2
        self.motor_right = wpilib.Victor(1)

        # gobbler for controller 6
        self.motor_gobbler = wpilib.Victor(2)

        # controller 5
        self.motor_shooter = wpilib.Victor(3)

        # controller 7 and 8
        self.motor_climber = wpilib.Victor(4)

        #conroller 9
        self.motor_mooover = wpilib.Victor(5)

        #gear servo
        self.motor_gear = wpilib.Victor(6)

        self.speed_gobbler = False
        self.button_gobbler = False
        self.speed_shooter = 0
        self.speed_climber = 0
        self.speed_mooover = 0
        self.button_servo = False
        self.gear_servo = False

    def disabled(self):
        '''Called when the robot is disabled'''
        while self.isDisabled():
            wpilib.Timer.delay(0.01)

    def autonomous(self):

        if 0:
            self.autonomous_straight()
        else:
            self.autonomous_diagonal()

    def autonomous_straight(self):
        '''Called when autonomous mode is enabled'''

        t0 = time()

        slow_forward = 0.25

        t_forward_time = 6.5
        t_spin_time = 11
        t_shoot_time = 11.5


        while self.isAutonomous() and self.isEnabled():
            t = time() - t0

            if t < t_forward_time:

                self.motor_left.set(slow_forward)
                self.motor_right.set(-slow_forward)
                self.motor_gobbler.set(1.0)

            elif t < t_spin_time:
                self.motor_left.set(2 * slow_forward)
                self.motor_right.set(2 * slow_forward)
                self.motor_shooter.set(-1.0)

            elif t < t_shoot_time:
                self.motor_mooover.set(.5)

            else:
                self.full_stop()
                self.motor_gear.set(-1.0)

            wpilib.Timer.delay(0.01)

        self.full_stop()

    def autonomous_diagonal(self):
        '''Called when autonomous mode is enabled'''

        t0 = time()

        slow_forward = 0.25
        fast_forward = 0.4

        t_forward_time = .6
        t_turn_time = 1.2
        t_forward_time2 = 3.1
        t_turn_time2 = 3.8
        t_forward_time3 = 7.5
        t_spin_time = 11
        t_shoot_time = 11.8


        while self.isAutonomous() and self.isEnabled():
            t = time() - t0

            if t < t_forward_time:

                self.motor_left.set(slow_forward)
                self.motor_right.set(-slow_forward)
                self.motor_gobbler.set(1.0)

            elif t < t_turn_time:
                self.motor_left.set(fast_forward)
                self.motor_right.set(fast_forward)

            elif t < t_forward_time2:
                self.motor_left.set(fast_forward)
                self.motor_right.set(-fast_forward)

            elif t < t_turn_time2:
                 self.motor_left.set(-slow_forward)
                 self.motor_right.set(-slow_forward)

            elif t < t_forward_time3:
                self.motor_left.set(slow_forward)
                self.motor_right.set(-slow_forward)

            elif t < t_spin_time:
                self.motor_left.set(fast_forward)
                self.motor_right.set(fast_forward)
                self.motor_shooter.set(-1.0)

            elif t < t_shoot_time:
                self.motor_mooover.set(.5)

            else:
                self.full_stop()
                self.motor_gear.set(-1.0)

            wpilib.Timer.delay(0.01)

        self.full_stop()

    def full_stop(self):
        self.motor_left.set(0.0)
        self.motor_right.set(0.0)
        self.motor_gobbler.set(0.0)
        self.motor_shooter.set(0.0)
        self.motor_mooover.set(0.0)
        self.motor_climber.set(0.0)

    def operatorControl(self):
        '''Runs the motor from a joystick.'''
        logging.info('op-control satrted')

        while self.isOperatorControl() and self.isEnabled():

            #logging.info(", ".join("%d: %4.2f" % (i, self.stick.getRawAxis(i)) for i in range(6)))
            #logging.info(",".join(str(self.stick.ds.joystickAxes[0].axes[i]) for i in range(12)))
            
            x = .75 * self.stick.getX()
            y = self.stick.getY()


            # gobbler
            gobbler_button_press = bool(self.stick.getRawButton(4))
            if not self.button_gobbler and gobbler_button_press:
                # rising edge
                self.speed_gobbler = not self.speed_gobbler
            self.button_gobbler = gobbler_button_press

            # shooter
            #the shooter is fined tuned so that once it reaches .615 it can increase or decrease to a limit
            if self.stick.getRawButton(5) and self.speed_shooter == 0:
                self.speed_shooter = .57
            if self.stick.getRawButton(5) and self.speed_shooter < .8:
                self.speed_shooter +=.003
            elif self.stick.getRawButton(6) and self.speed_shooter > .45:
                self.speed_shooter -= .003
            if self.speed_shooter <.45 or self.speed_shooter ==.45:
                    self.speed_shooter = 0

            #servo for gear holder
            gear_button_press = bool(self.stick.getRawButton(10))
            if not self.button_servo and gear_button_press:
                #rising edge
                self.gear_servo = not self.gear_servo
            self.button_servo = gear_button_press

            # climber
            if self.stick.getRawButton(8) and self.speed_climber < .8:
                self.speed_climber += .01
            elif self.stick.getRawButton(7) and self.speed_climber > -.2:
                self.speed_climber -= .01
            if self.stick.getRawButton(1):
                self.speed_climber = 0

            # this controls the movement of balls in the box
            if self.stick.getRawButton(3):
                self.speed_mooover = .5
                
            else :
                self.speed_mooover = 0
                
           # logging.info('x=%s, y=%s, gobbler=%s, shooter=%s' % (x, y, self.speed_gobbler, self.speed_shooter))

            # gobbler reverse
            if self.stick.getRawButton(2):
                gobbler = -.5
            else:
                gobbler = 1.0 if self.speed_gobbler else 0.0

            increase_speed = self.stick.getZ()
            
            r = curve(max(min(x + y, 1.0), -1.0))
            l = curve(max(min(y - x, 1.0), -1.0))
            
            self.motor_left.set((-.5 * l) * (1 + increase_speed))
            self.motor_right.set((.5 * r ) * (1 + increase_speed))
            self.motor_gobbler.set(gobbler )
            self.motor_shooter.set(-self.speed_shooter)
            self.motor_climber.set(-self.speed_climber)
            self.motor_mooover.set(self.speed_mooover)
            self.motor_gear.set(-1.0 if self.gear_servo else 0.0)

            wpilib.Timer.delay(self.kUpdatePeriod)  # wait 5ms to the next update



if __name__ == "__main__":
    wpilib.run(MyRobot)
