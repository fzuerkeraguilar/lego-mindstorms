#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.parameters import Port, Button
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import ImageFile

from modes.mode import Mode
from modes.linefollower import LineFollower
from modes.boxpusher import BoxPusher
from modes.bridgecrosser import BridgeCrosser
from modes.pointfinder import PointFinder
from modes.debug import Debug
from turning_distance_sensor import TurningDistanceSensor
from menu import Menu


class Main:
    def __init__(self):
        self.ev3 = EV3Brick()
        self.r_motor = Motor(Port.B)
        self.l_motor = Motor(Port.A)
        self.distance_motor = Motor(Port.C)
        self.ultrasonic_sensor = UltrasonicSensor(Port.S4)
        self.drivebase = DriveBase(
            self.l_motor, self.r_motor, wheel_diameter=33, axle_track=192
        )
        self.color_sensor = ColorSensor(Port.S1)
        self.r_touch_sensor = TouchSensor(Port.S2)
        # self.l_touch_sensor = TouchSensor(Port.S3)
        self.distance_sensor = TurningDistanceSensor(self.distance_motor, self.ultrasonic_sensor)

    def main(self):
        modes = [
            ("Line Follower", LineFollower(
                                self.ev3,
                                self.drivebase,
                                self.r_motor,
                                self.l_motor,
                                self.color_sensor,
                                self.distance_sensor,
                            )),
            ("Box Pusher", BoxPusher(
                                self.ev3,
                                self.drivebase,
                                self.color_sensor,
                                self.distance_sensor,
                                self.r_touch_sensor,
                                self.r_motor,
                                self.l_motor,
                            )),
            ("Bridge Crosser", BridgeCrosser(
                                self.ev3,
                                self.drivebase,
                                self.color_sensor,
                                self.distance_sensor,
                            )),
            ("Point Finder", PointFinder(
                                self.ev3,
                                self.drivebase,
                                self.color_sensor,
                                self.distance_sensor,
                            )),
            ("Debug", Debug(
                                self.ev3,
                                self.drivebase,
                                self.r_motor,
                                self.l_motor,
                                self.color_sensor,
                                self.r_touch_sensor,
                                self.distance_sensor,
                                self.distance_motor,
                            ))
        ]

        menu = Menu(self.ev3, modes)
        program = menu.show()

        if program == None:
            return
        else:
            program.run()

if __name__ == "__main__":
    Main().main()
