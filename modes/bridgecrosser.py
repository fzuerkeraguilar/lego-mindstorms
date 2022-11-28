from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor, GyroSensor
from modes.mode import Mode


class BridgeCrosser(Mode):

    RAMP_ANGLE = 15
    INITIAL_SPEED = 50

    def __init__(self, color_sensor, distance_sensor, config, speed=INITIAL_SPEED):
        super().__init__(color_sensor, distance_sensor, config, speed)
        self.drivebase = config.get_drivebase(clean=True)

    def run(self):
        self.drivebase.straight(1050)
        self.drivebase.turn(-90)
        self.drivebase.straight(1260)
        self.drivebase.turn(-90)
        self.drivebase.straight(1000)
