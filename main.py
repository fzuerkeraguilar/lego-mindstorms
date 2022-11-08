#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Button
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import ImageFile

from linefollower import LineFollower
from debug import Debug
from turning_distance_sensor import TurningDistanceSensor

class Main:

    def __init__(self):
        self.ev3 = EV3Brick()
        self.right_motor = Motor(Port.B)
        self.left_motor = Motor(Port.A)
        self.distance_drive = Motor(Port.C)
        self.drive_base = DriveBase(left_motor, right_motor, wheel_diameter=33, axle_track=185)
        self.color_sensor = ColorSensor(Port.S1)
        self.r_touch_sensor = TouchSensor(Port.S2)
        self.l_touch_sensor = TouchSensor(Port.S3)
        self.distance_sensor = TurningDistanceSensor(Port.C, Port.S4)

    def main():
        # Menu to select the program to run
        ev3.screen.load_image(ImageFile.QUESTION_MARK)
        ev3.speaker.beep()
        # Wait for a button to be pressed
        while not any(ev3.buttons.pressed()):
            wait(10)
            if Button.CENTER in ev3.buttons.pressed():
                ev3.speaker.beep()
                Debug(self.drive_base, self.color_sensor, self.r_touch_sensor, self.distance_sensor, self.ev3,
                    self.right_motor, self.left_motor, self.distance_drive).run()
                break

            elif Button.UP in ev3.buttons.pressed():
                ev3.speaker.beep()
                LineFollower(self.drive_base, self.right_motor, self.left_motor, self.color_sensor, self.r_touch_sensor, self.distance_sensor, self.ev3).run()
                break

            elif Button.RIGHT in ev3.buttons.pressed():
                ev3.speaker.beep()
                break

            elif Button.DOWN in ev3.buttons.pressed():
                ev3.speaker.beep()
                break

            elif Button.LEFT in ev3.buttons.pressed():
                ev3.speaker.beep()
                break

if __name__ == "__main__":
    Main().main()
