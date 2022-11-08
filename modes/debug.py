from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                    InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile


class Debug:

    def __init__(self, drivebase, color_sensor, touch_sensor, distance_sensor, hub, right_motor, left_motor, distance_drive, speed=100):
        self.drivebase = drivebase
        self.color_sensor = color_sensor
        self.touch_sensor = touch_sensor
        self.distance_sensor = distance_sensor
        self.hub = hub
        self.distance_drive = distance_drive
        self.speed = speed
        self.right_motor = right_motor
        self.left_motor = left_motor

    def run(self):
        self.right_motor.reset_angle(0)
        self.left_motor.reset_angle(0)
        self.right_motor.run_time(600, 1300, then=Stop.BRAKE, wait=False)
        self.left_motor.run_time(-600, 1300, then=Stop.BRAKE, wait=False)
        while True:
            pass
    
        # while Button.UP not in self.hub.buttons.pressed():
        #     # direction = 1
        #     # self.hub.screen.print(self.color_sensor.reflection())
        #     # self.drivebase.drive(100, 0)
        #     # self.distance_drive.reset_angle(0)
        #     # self.distance_drive.run_angle(100, 90, wait=True)
        #     # wait(500)
        #     # self.distance_drive.run_angle(100, -90, wait=True)
        #     # wait(500)
        #     self.drivebase.turn(360)
