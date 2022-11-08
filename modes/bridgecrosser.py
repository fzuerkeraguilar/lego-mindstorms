from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor, GyroSensor


class BridgeCrosser:

    RAMP_ANGLE = 15


    def __init__(self, drivebase, color_sensor, touch_sensor, gyro_sensor, speed=100):
        self.drivebase = drivebase
        self.color_sensor = color_sensor
        self.touch_sensor = touch_sensor
        self.gyro_sensor = gyro_sensor
        self.speed = speed
        self.gyro_sensor.reset_angle(0)

    def run(self):
        
