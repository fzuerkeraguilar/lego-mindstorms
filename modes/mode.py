from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import (
    Motor,
)
from pybricks.ev3devices import TouchSensor, ColorSensor
from turning_distance_sensor import TurningDistanceSensor


class Mode:
    def __init__(self, color_sensor, distance_sensor, config, speed=100):
        self.hub = EV3Brick()
        self.drivebase = config.get_drivebase()
        self.color_sensor = color_sensor
        self.distance_sensor = distance_sensor
        self.speed = speed
        pass

    def run():
        pass
