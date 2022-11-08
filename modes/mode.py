from pybricks.hubs import EV3Brick
from pybricks.parameters import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor 
from turning_distance_sensor import TurningDistanceSensor

class Mode:

    def __init__(self, ev3_hub, drivebase, color_sensor, distance_sensor, speed):
        self.hub = ev3_hub
        self.drivebase = drive_base
        self.color_sensor = color_sensor
        self.distance_sensor = distance_sensor
        self.speed = speed
        pass

    def run():
        pass