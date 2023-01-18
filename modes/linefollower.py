from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Stop, Button
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, UltrasonicSensor
from pybricks.tools import wait, StopWatch, DataLog
from modes.mode import Mode
from math import floor


class LineFollower(Mode):
    BLACK = 6
    WHITE = 35
    THRESHOLD = (BLACK + WHITE) / 2
    GAIN = 3

    LAST_FOUND_RIGHT = True

    INITIAL_SPEED = 70
    TOP_SPEED = 200
    STEP_SIZE = 10
    WAIT_TIME = 5
    INITIAL_TURN = 50
    RIGHT_ANGLE_TURN_TIME = 2000
    NINETY_TURN_TIME = 575

    def __init__(
        self,
        color_sensor,
        distance_sensor,
        touch_sensor,
        config,
        speed=INITIAL_SPEED,
    ):
        super().__init__(color_sensor, distance_sensor, config, speed)
        self.r_motor = self.drivebase.right
        self.l_motor = self.drivebase.left
        self.touch_sensor = touch_sensor
        self.config = config
        self.WHITE, self.BLACK = self.config.get_wb()
        self.THRESHOLD = (self.BLACK + self.WHITE) / 2
        self.logger = DataLog("timestamp", "reflection", "speed", "turn_rate", "distance", "LAST_FOUND_RIGHT")
        self.watch = StopWatch()

    def follow_line(self):
        while True:
            if self.touch_sensor.pressed():
                self.avoid_obstacle()

            # Calculate the deviation from the threshold.
            reflection = self.color_sensor.reflection()

            if reflection <= self.BLACK:
                self.speed = self.INITIAL_SPEED
                # blue line is "Black" for reflection. Check here whether we lost line or found blue line
                if self.color_sensor.color() == Color.BLUE:
                    self.drivebase.stop()
                    return

                if not self.find_line_direct():
                    self.bridge_gap()

                self.logger.log(self.watch.time(), reflection, -1, 0, self.drivebase.distance(), self.LAST_FOUND_RIGHT)
            else:
                deviation = reflection - self.THRESHOLD
                if abs(deviation) < 5:
                    self.speed = min(self.TOP_SPEED, self.speed + 2)
                if abs(deviation) > 10:
                    self.speed = max(self.INITIAL_SPEED, self.speed * 0.8)

                turn_rate = self.GAIN * deviation
                self.drivebase.drive(self.speed, turn_rate)
                self.logger.log(self.watch.time(), reflection, self.speed, turn_rate, self.drivebase.distance(), self.LAST_FOUND_RIGHT)

    def avoid_obstacle(self):
        self.drivebase.stop()
        self.drivebase.settings(self.speed, None, self.speed, None)
        self.drivebase.straight(-50)
        self.drivebase.turn(90)
        self.drivebase.straight(200)
        self.drivebase.turn(-90)
        self.drivebase.straight(360)
        self.drivebase.turn(-90)
        self.drivebase.straight(200)
        self.drivebase.turn(90)
        self.drivebase.straight(-80)
        self.drivebase.straight(10)
        self.find_line_direct()

    def turn_and_find_line(self, speed, turn_right, ninety_degrees=1):
        self.hub.speaker.beep()
        self.drivebase.stop()
        self.r_motor.hold()
        self.l_motor.hold()
        self.r_motor.reset_angle(0)
        self.l_motor.reset_angle(0)
        if turn_right:
            self.r_motor.run_angle(speed, - self.NINETY_TURN_TIME * ninety_degrees, wait=False)
            self.l_motor.run_angle(speed, self.NINETY_TURN_TIME * ninety_degrees, wait=False)
            while self.r_motor.angle() > - self.NINETY_TURN_TIME * ninety_degrees and self.l_motor.angle() < self.NINETY_TURN_TIME * ninety_degrees:
                if self.color_sensor.reflection() > self.THRESHOLD + 5:
                    self.r_motor.hold()
                    self.l_motor.hold()
                    return True
        else:
            self.r_motor.run_angle(speed, self.NINETY_TURN_TIME * ninety_degrees, wait=False)
            self.l_motor.run_angle(speed, - self.NINETY_TURN_TIME * ninety_degrees, wait=False)
            while self.r_motor.angle() < self.NINETY_TURN_TIME * ninety_degrees and self.l_motor.angle() > - self.NINETY_TURN_TIME * ninety_degrees:
                if self.color_sensor.reflection() > self.THRESHOLD + 5:
                    self.r_motor.hold()
                    self.l_motor.hold()
                    return True
        self.r_motor.hold()
        self.l_motor.hold()
        return False

    def find_line_direct(self):
        if self.turn_and_find_line(800, self.LAST_FOUND_RIGHT):
            self.LAST_FOUND_RIGHT = self.LAST_FOUND_RIGHT
            return True
        elif self.turn_and_find_line(800, not self.LAST_FOUND_RIGHT, ninety_degrees=2):
            self.LAST_FOUND_RIGHT = not self.LAST_FOUND_RIGHT
            return True
        return self.turn_and_find_line(800, self.LAST_FOUND_RIGHT)

    def bridge_gap(self):
        self.drivebase.reset()
        self.drivebase.drive(self.TOP_SPEED, 0)
        while self.drivebase.distance() < 160:
            if self.color_sensor.reflection() > self.THRESHOLD + 3:
                break
        self.drivebase.stop()

    def run(self):
        self.distance_sensor.set_up()
        self.watch.reset()
        self.hub.speaker.beep()
        self.follow_line()
