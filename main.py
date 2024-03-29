#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor
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
from multitouch_sensor import MultitouchSensor
from menu import Menu


class Main:
    def __init__(self):
        self.ev3 = EV3Brick()
        self.l_motor = Motor(Port.A)
        self.r_motor = Motor(Port.B)
        self.distance_motor = Motor(Port.C)
        self.ultrasonic_sensor = UltrasonicSensor(Port.S4)
        self.color_sensor = ColorSensor(Port.S1)
        self.left_touch_sensor = TouchSensor(Port.S3)
        self.right_touch_sensor = TouchSensor(Port.S2)
        self.touch_sensor = MultitouchSensor(self.left_touch_sensor, self.right_touch_sensor)
        self.distance_sensor = TurningDistanceSensor(
            self.distance_motor, self.ultrasonic_sensor
        )
        self.config = Calibration(self.l_motor, self.r_motor, self.color_sensor)

    def main(self):
        modes = [
            (
                "Line Follower",
                LineFollower(
                    self.color_sensor,
                    self.distance_sensor,
                    self.touch_sensor,
                    self.config,
                ),
                1
            ),
            (
                "Box Pusher",
                BoxPusher(
                    self.color_sensor,
                    self.distance_sensor,
                    self.touch_sensor,
                    self.config,
                ),
                2
            ),
            (
                "Bridge Crosser",
                BridgeCrosser(
                    self.color_sensor,
                    self.distance_sensor,
                    self.touch_sensor,
                    self.config,
                ),
                3
            ),
            (
                "Point Finder",
                PointFinder(
                    self.color_sensor,
                    self.distance_sensor,
                    self.touch_sensor,
                    self.config,
                ),
                None
            ),
            (
                "Debug",
                Debug(
                    self.color_sensor,
                    self.distance_sensor,
                    self.touch_sensor,
                    self.config,
                ),
                None
            ),
            (
                "Calibration",
                Calibration(self.l_motor, self.r_motor, self.color_sensor),
                None
            ),
        ]

        menu = Menu(self.ev3, modes)
        next_program = None
        while True:
            program, next_program = menu.show(autoselect=next_program)
            self.ev3.speaker.beep()

            if program == None:
                return
            else:
                if program.run() == False:
                    next_program = None
                    self.ev3.speaker.beep(400)
                    self.ev3.screen.print("Stopped. Press Up")
                    while Button.UP not in self.ev3.buttons.pressed():
                        pass
                    
                # try:
                #     if program.run() == False:
                #         next_program = None
                # except Exception as e:
                #     self.ev3.speaker.beep()
                #     self.ev3.screen.print(e)
                #     wait(5000)
                #     next_program = None

if __name__ == "__main__":
    Main().main()
