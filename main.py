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
from modes.calibration import Calibration
from turning_distance_sensor import TurningDistanceSensor


class Main:
    def __init__(self):
        self.ev3 = EV3Brick()
        self.l_motor = Motor(Port.A)
        self.r_motor = Motor(Port.B)

        self.color_sensor = ColorSensor(Port.S1)
        self.r_touch_sensor = TouchSensor(Port.S2)
        self.distance_sensor = TurningDistanceSensor(Port.C, Port.S4)
        self.config = Calibration(self.hub, self.l_motor, self.r_motor)

    def main(self):
        # Menu to select the program to run
        options = [
            "Line Follower",
            "Box Pusher",
            "Bridge Crosser",
            "Point Finder",
            "Complete Run",
            "Debug",
            "Calibration",
        ]
        option = 0

        self.ev3.screen.clear()
        self.ev3.screen.print("Select a program to run:")
        self.ev3.screen.print(options[option])
        while True:
            wait(150)
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
                    LineFollower(
                        self.color_sensor,
                        self.distance_sensor,
                        self.config,
                    ).run()
                elif option == 1:
                    BoxPusher(
                        self.color_sensor,
                        self.distance_sensor,
                        self.r_touch_sensor,
                        self.config,
                    ).run()
                elif option == 2:
                    BridgeCrosser(
                        self.color_sensor,
                        self.distance_sensor,
                        self.config,
                    ).run()
                elif option == 3:
                    PointFinder(
                        self.color_sensor,
                        self.distance_sensor,
                        self.config,
                    ).run()
                elif option == 4:
                    LineFollower(
                        self.color_sensor,
                        self.distance_sensor,
                        self.config,
                    ).run()
                    BoxPusher(
                        self.color_sensor,
                        self.distance_sensor,
                        self.r_touch_sensor,
                        self.config,
                    ).run()
                    BridgeCrosser(
                        self.color_sensor,
                        self.distance_sensor,
                        self.config,
                    ).run()
                    PointFinder(
                        self.color_sensor,
                        self.distance_sensor,
                        self.config,
                    ).run()
                elif option == 5:
                    Debug(
                        self.color_sensor,
                        self.distance_sensor,
                        self.r_touch_sensor,
                        self.config,
                    ).run()
                elif option == 6:
                    self.config.run()
                self.ev3.screen.clear()
                self.ev3.screen.print("Select a program to run:")
                self.ev3.screen.print(options[option])
            elif Button.CENTER in self.ev3.buttons.pressed():
                break


if __name__ == "__main__":
    Main().main()
