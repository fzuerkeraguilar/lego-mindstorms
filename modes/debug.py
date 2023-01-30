from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor
)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
from modes.mode import Mode


class Debug(Mode):
    def __init__(
        self,
        color_sensor,
        distance_sensor,
        touch_sensor,
        config,
        speed=100,
    ):
        super().__init__(color_sensor, distance_sensor, config, speed)
        self.touch_sensor = touch_sensor
        self.left_motor = self.drivebase.left
        self.right_motor = self.drivebase.right

    def run(self):

        logger = DataLog("timestamp", "distance")
        watch = StopWatch()
        self.distance_sensor.set_up()
        self.distance_sensor.set_angle(80)
        self.drivebase.drive(50, 0)
        watch.reset()
        while True:
            dist = self.distance_sensor.distance()
            logger.log(watch.time(), dist)


        # self.right_motor.reset_angle(0)
        # self.left_motor.reset_angle(0)
        # self.right_motor.run_time(600, 1300, then=Stop.BRAKE, wait=False)
        # self.left_motor.run_time(-600, 1300, then=Stop.BRAKE, wait=False)

        while True:
            self.drivebase.drive(100, 360)

    def rgb_to_hsv(self, rgb):
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        r = r / 255
        g = g / 255
        b = b / 255
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin
        if delta == 0:
            h = 0
        elif cmax == r:
            h = 60 * (((g - b) / delta) % 6)
        elif cmax == g:
            h = 60 * (((b - r) / delta) + 2)
        elif cmax == b:
            h = 60 * (((r - g) / delta) + 4)
        if cmax == 0:
            s = 0
        else:
            s = delta / cmax
        v = cmax
        return h, s, v
