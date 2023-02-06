from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor
from modes.mode import Mode
from pybricks.tools import wait

import random


class PointFinder(Mode):
    INITIAL_SPEED = 700
    INITIAL_SIDE_LENGTH = 1000
    BOX_LENGTH = 980
    BOX_WIDTH = 950
    red_found = False
    white_found = False

    def __init__(self, color_sensor, distance_sensor, touch_sensor, config, speed=INITIAL_SPEED):
        super().__init__(color_sensor, distance_sensor, config, speed)
        self.touch_sensor = touch_sensor
        self.red_found = False
        self.white_found = False

    def circle_search(self):
        distances = [self.BOX_LENGTH, self.BOX_WIDTH]
        self.distance_sensor.set_up()
        while distances[0] > 0 and distances[1] > 0:
            for i in range(0, 2):
                wall_distance = self.distance_sensor.distance()
                while self.drivebase.distance() < distances[i] and not self.touch_sensor.pressed():
                    self.drive_guided_straight(wall_distance)
                    if self.check_color():
                        return
                self.drivebase.stop()
                if self.touch_sensor.pressed():
                    distances[i] = self.drivebase.distance()
                    self.drivebase.straight(-30)
                distances[i] -= 60
                self.drivebase.turn(-90)
                self.drivebase.reset()

    def drive_guided_straight(self, wall_distance_mm):
        current_distance = self.distance_sensor.distance()
        if current_distance < wall_distance_mm or current_distance > self.BOX_LENGTH:
            self.drivebase.drive(self.INITIAL_SPEED, -3)
        else:
            self.drivebase.drive(self.INITIAL_SPEED, 3)
            

    def check_color(self):
        color = self.color_sensor.color()
        if not self.red_found and color == Color.RED:
            self.red_found = True
            self.hub.speaker.beep()
            self.hub.screen.print("Found red!")
        if not self.white_found and color == Color.WHITE:
            self.white_found = True
            self.hub.speaker.beep()
            self.hub.screen.print("Found white!")
        if self.red_found and self.white_found:
            self.hub.speaker.beep()
            self.hub.screen.print("Found both!")
            self.drivebase.stop()
            return True
        return False

    def run(self):
        self.drivebase.reset()
        self.drivebase.settings(self.INITIAL_SPEED, 1000, self.INITIAL_SPEED, 1000)
        self.drivebase.straight(80)
        self.distance_sensor.set_up()
        self.circle_search()
