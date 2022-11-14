from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor, GyroSensor
from modes.mode import Mode

class BridgeCrosser(Mode):

    RAMP_ANGLE = 15
    INITIAL_SPEED = 50

    def __init__(self, ev3_hub, drivebase, color_sensor, distance_sensor,
    speed=self.INITIAL_SPEED):
        super().__init__(ev3_hub, drivebase, color_sensor, distance_sensor, speed)

    def run(self):
        pass
        
