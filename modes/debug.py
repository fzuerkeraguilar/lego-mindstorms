from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                    InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
from modes.mode import Mode


class Debug(Mode):

    def __init__(self, ev3_hub, drivebase, right_motor, left_motor,
    color_sensor, touch_sensor, distance_sensor, distance_drive, speed=100):
        super().__init__(ev3_hub, drivebase, color_sensor, distance_sensor, speed)
        self.touch_sensor = touch_sensor
        self.distance_drive = distance_drive
        self.right_motor = right_motor
        self.left_motor = left_motor

    def run(self):
        # self.right_motor.reset_angle(0)
        # self.left_motor.reset_angle(0)
        # self.right_motor.run_time(600, 1300, then=Stop.BRAKE, wait=False)
        # self.left_motor.run_time(-600, 1300, then=Stop.BRAKE, wait=False)

        
        while True:
            rgb = self.color_sensor.rgb()
            #h, s, v = self.rgb_to_hsv(rgb)
            self.hub.screen.print(rgb)
            #self.hub.screen.print(v)
        
    def rgb_to_hsv(self, rgb):
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        r = r/255
        g = g/255
        b = b/255
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin
        if delta == 0:
            h = 0
        elif cmax == r:
            h = 60 * (((g-b)/delta) % 6)
        elif cmax == g:
            h = 60 * (((b-r)/delta) + 2)
        elif cmax == b:
            h = 60 * (((r-g)/delta) + 4)
        if cmax == 0:
            s = 0
        else:
            s = delta/cmax
        v = cmax
        return h, s, v

    
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
