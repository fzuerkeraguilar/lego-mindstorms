from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor


class LineFollower:
    BLACK = 10
    WHITE = 45
    THRESHOLD = (BLACK + WHITE) / 2

    GAIN = 1.2

    def __init__(self, drivebase, color_sensor, touch_sensor, speed=100):
        self.drivebase = drivebase
        self.color_sensor = color_sensor
        self.touch_sensor = touch_sensor
        self.speed = speed


    def follow_line(self):
        while True:
            # Calculate the deviation from the threshold.
            deviation = line_sensor.reflection() - threshold
            # Calculate the turn rate.
            turn_rate = PROPORTIONAL_GAIN * deviation
            # Set the drive base speed and turn rate.
            robot.drive(DRIVE_SPEED, turn_rate)
            # You can wait for a short time or do other things in this loop.
            wait(10)

    
        



    def avoid_object(self):
        self.drivebase.stop()
        self.drivebase.drive_time(-100, 0, 1000)
        self.drivebase.drive_time(0, 100, 500)
        self.drivebase.drive_time(100, 0, 1000)
        self.drivebase.drive_time(0, -100, 500)
        self.drivebase.stop()
    
    def run(self):
        self.follow_line()
        