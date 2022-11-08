from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor, GyroSensor

class PointFinder (Mode):

    def __init__(self):
        self.ev3 = EV3Brick()
        self.drivebase = DriveBase(left_motor=Motor(Port.B), right_motor=Motor(Port.C), wheel_diameter=55.5, axle_track=104)
        self.color_sensor = ColorSensor(Port.S1)
        self.touch_sensor = TouchSensor(Port.S2)
        self.gyro_sensor = GyroSensor(Port.S3)
        self.speed = 100
        self.gyro_sensor.reset_angle(0)