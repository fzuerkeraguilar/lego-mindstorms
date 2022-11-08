#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Button
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import ImageFile

from modes.linefollower import LineFollower
from modes.debug import Debug
from turning_distance_sensor import TurningDistanceSensor

class Main:

    def __init__(self):
        self.ev3 = EV3Brick()
        self.r_motor = Motor(Port.B)
        self.l_motor = Motor(Port.A)
        self.distance_drive = Motor(Port.C)
        self.drive_base = DriveBase(self.l_motor, self.r_motor, wheel_diameter=33, axle_track=185)
        self.color_sensor = ColorSensor(Port.S1)
        self.r_touch_sensor = TouchSensor(Port.S2)
        self.l_touch_sensor = TouchSensor(Port.S3)
        self.distance_sensor = TurningDistanceSensor(Port.C, Port.S4)

    def main():
        # Menu to select the program to run
        options = ["Line Follower", "Box Pusher", "Bridge Crosser", "Point Finder", "Debug"]
        option = 0

        self.ev3.screen.clear()
        self.ev3.screen.print("Select a program to run:")
        self.ev3.screen.print(options[option])
        while True:
            if Button.UP in self.ev3.buttons.pressed():
                option = (option - 1) % len(options)
                self.ev3.screen.clear()
                self.ev3.screen.print("Select a program to run:")
                self.ev3.screen.print(options[option])
            elif Button.DOWN in self.ev3.buttons.pressed():
                option = (option + 1) % len(options)
                self.ev3.screen.clear()
                self.ev3.screen.print("Select a program to run:")
                self.ev3.screen.print(options[option])
            elif Button.RIGHT in self.ev3.buttons.pressed():
                self.ev3.screen.clear()
                self.ev3.screen.print("Running " + options[option])
                if option == 0:
                    LineFollower(self.ev3, self.drivebase, self.r_motor, self.l_motor, self.color_sensor, self.distance_sensor).run()
                elif option == 1:
                    BoxPusher(self.ev3, self.drivebase, self.color_sensor, self.distance_sensor, self.r_touch_sensor).run()
                elif option == 2:
                    BridgeCrosser(self.ev3, self.drivebase, self.color_sensor, self.distance_sensor).run()
                elif option == 3:
                    PointFinder(self.ev3, self.drivebase, self.color_sensor, self.distance_sensor).run()
                elif option == 4:
                    Debug(self.ev3, self.drivebase, self.r_motor, self.l_motor,
                    self.color_sensor, self.r_touch_sensor, self.distance_sensor, self.distance_drive).run()
                self.ev3.screen.clear()
                self.ev3.screen.print("Select a program to run:")
                self.ev3.screen.print(options[option])
            elif Button.CENTER in self.ev3.buttons.pressed():
                break
                

if __name__ == "__main__":
    Main().main()
