from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Stop, Button
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, UltrasonicSensor
from pybricks.tools import wait, StopWatch
from modes.mode import Mode


class LineFollower(Mode):
    BLACK = 6
    WHITE = 35
    THRESHOLD = (BLACK + WHITE) / 2
    GAIN = 3

    LAST_FOUND_RIGHT = False

    INITIAL_SPEED = 60
    TOP_SPEED = 100
    STEP_SIZE = 10
    WAIT_TIME = 5
    INITIAL_TURN = 50
    RIGHT_ANGLE_TURN_TIME = 2000

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

    def follow_line(self):
        if self.touch_sensor.pressed():
            self.avoid_obstacle()

        # Calculate the deviation from the threshold.
        reflection = self.color_sensor.reflection()
        deviation = reflection - self.THRESHOLD

        if reflection <= self.BLACK:
            self.speed = self.INITIAL_SPEED
            # blue line is "Black" for reflection. Check here whether we lost line or found blue line
            if self.color_sensor.color() == Color.BLUE:
                self.drivebase.stop()
                return False

            if not self.find_line_direct():
                self.drivebase.straight(150)

        self.speed = min(self.TOP_SPEED, self.speed + 1)
        if abs(deviation) > 7:
            self.speed = max(self.INITIAL_SPEED, self.speed / 2)

        turn_rate = self.GAIN * deviation
        self.drivebase.drive(self.speed, turn_rate)
        return True

    def avoid_obstacle(self):
        self.drivebase.stop()
        self.drivebase.straight(-50)
        self.drivebase.turn(90)
        self.drivebase.straight(200)
        self.drivebase.turn(-90)
        self.drivebase.straight(370)
        self.drivebase.turn(-90)
        self.drivebase.straight(200)
        self.drivebase.turn(90)
        self.drivebase.straight(-50)
        self.find_line_direct()

    def turn_and_find_line(self, speed, time, turn_right):
        watch = StopWatch()

        if turn_right:
            speed_right = -speed
            speed_left = speed

        else:
            speed_right = speed
            speed_left = -speed

        self.hub.speaker.beep()
        self.drivebase.stop()

        self.r_motor.run_time(speed_right, time, then=Stop.HOLD, wait=False)
        self.l_motor.run_time(speed_left, time, then=Stop.HOLD, wait=False)
        watch.reset()
        while watch.time() < time + 100:
            if self.color_sensor.reflection() > self.THRESHOLD + 3:
                self.r_motor.stop()
                self.l_motor.stop()
                return True
            pass

        return False

    def find_line_direct(self):
        
        if self.LAST_FOUND_RIGHT:
            if self.turn_and_find_line(300,self.RIGHT_ANGLE_TURN_TIME , True):
                self.LAST_FOUND_RIGHT = True
                return True
            elif self.turn_and_find_line(300, 2 * self.RIGHT_ANGLE_TURN_TIME, False):
                self.LAST_FOUND_RIGHT = False
                return True
            self.r_motor.run_time(-300, self.RIGHT_ANGLE_TURN_TIME, then=Stop.HOLD, wait=False)
            self.l_motor.run_time(300, self.RIGHT_ANGLE_TURN_TIME, then=Stop.HOLD, wait=True)
        else:
            if self.turn_and_find_line(300, self.RIGHT_ANGLE_TURN_TIME, False):
                self.LAST_FOUND_RIGHT = False
                return True
            elif self.turn_and_find_line(300, 2 * self.RIGHT_ANGLE_TURN_TIME, True):
                self.LAST_FOUND_RIGHT = True
                return True
            self.r_motor.run_time(300, self.RIGHT_ANGLE_TURN_TIME, then=Stop.HOLD, wait=False)
            self.l_motor.run_time(-300, self.RIGHT_ANGLE_TURN_TIME, then=Stop.HOLD, wait=True)

        return False

    def run(self):
        while Button.CENTER not in self.hub.buttons.pressed():
            if not self.follow_line():
                break
