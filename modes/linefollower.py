from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Stop, Button
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, UltrasonicSensor
from pybricks.tools import wait, StopWatch
from modes.mode import Mode


class LineFollower(Mode):
    BLACK = 6
    WHITE = 42
    THRESHOLD = (BLACK + WHITE) / 2
    GAIN = 3

    INITIAL_SPEED = 60
    TOP_SPEED = 90
    STEP_SIZE = 10
    WAIT_TIME = 5
    INITIAL_TURN = 50
    END_COLOR = Color.BLUE

    def __init__(
        self,
        ev3_hub,
        drivebase,
        right_motor,
        left_motor,
        color_sensor,
        distance_sensor,
        speed=INITIAL_SPEED,
    ):
        super().__init__(ev3_hub, drivebase, color_sensor, distance_sensor, speed)
        self.right_motor = right_motor
        self.left_motor = left_motor

    def follow_line(self):
        if self.distance_sensor.distance() < 100:
            self.avoid_obstacle()

        # Calculate the deviation from the threshold.
        reflection = self.color_sensor.reflection()
        deviation = reflection - self.THRESHOLD
        rgb = self.color_sensor.rgb()
        if rgb[0] < 10 and rgb[1] < 30 and rgb[2] > 25:
            self.hub.speaker.beep()
            self.drivebase.stop()
            return True

        if reflection <= self.BLACK + 3:
            self.speed = self.INITIAL_SPEED
            if not self.find_line_direct():
                self.hub.speaker.beep(frequency=10000)
                self.drivebase.straight(150)

        self.speed = min(self.TOP_SPEED, self.speed + 1)
        if abs(deviation) > 7:
            self.speed = self.INITIAL_SPEED

        turn_rate = self.GAIN * deviation
        self.drivebase.drive(self.speed, turn_rate)
        return False

    def avoid_obstacle(self):
        self.drivebase.stop()
        self.drivebase.turn(90)
        self.drivebase.straight(200)
        self.drivebase.turn(-90)
        self.drivebase.straight(400)
        self.drivebase.turn(-90)
        self.drivebase.straight(200)
        self.drivebase.turn(90)
        self.find_line_direct()

    def turn_and_find_line(self, speed, time, turn_right):
        watch = StopWatch()
        watch.pause()
        watch.reset()
        if turn_right:
            speed_right = -speed
            speed_left = speed
            self.hub.screen.print("Turn right")

        else:
            speed_right = speed
            speed_left = -speed
            self.hub.screen.print("Turn left")

        self.hub.speaker.beep()
        self.drivebase.stop()

        self.right_motor.run_time(right_speed, time, then=Stop.HOLD, wait=False)
        self.left_motor.run_time(left_speed, time, then=Stop.HOLD, wait=False)

        while watch.time() < time + 100:
            if self.color_sensor.reflection() > self.THRESHOLD + 3:
                self.hub.screen.print("Found line 1")
                self.right_motor.stop()
                self.left_motor.stop()
                return True
            pass

        return False

    def find_line_direct(self):

        # watch = StopWatch()
        # watch.pause()
        # watch.reset()

        # self.hub.speaker.beep()
        # self.drivebase.stop()
        # self.hub.screen.print("Turn left")
        # self.right_motor.run_time(500, 1300, then=Stop.HOLD, wait=False)
        # self.left_motor.run_time(-500, 1300, then=Stop.HOLD, wait=False)
        # watch.resume()
        # while watch.time() < 1400:
        #     if self.color_sensor.reflection() > self.THRESHOLD + 3:
        #         self.hub.screen.print("Found line 1")
        #         self.right_motor.stop()
        #         self.left_motor.stop()
        #         return True
        #     pass

        if self.turn_and_find_line(500, 1300, True):
            return True

        if self.turn_and_find_line(500, 2600, False):
            return True

        self.right_motor.run_time(500, 1400, then=Stop.HOLD, wait=False)
        self.left_motor.run_time(-500, 1400, then=Stop.HOLD, wait=True)
        return False

    def find_line_drivebase(self):
        self.drivebase.stop()
        self.hub.screen.print(self.drivebase.heading_control.pid())
        self.hub.screen.print(self.drivebase.heading_control.limits())
        degrees = 0

        while degrees < self.INITIAL_TURN:
            self.drivebase.turn(self.STEP_SIZE)
            degrees += self.STEP_SIZE
            if self.color_sensor.reflection() > self.THRESHOLD + 3:
                return True
        self.drivebase.turn(-self.INITIAL_TURN)
        degrees = 0
        while degrees > -90:
            self.drivebase.turn(-self.STEP_SIZE)
            degrees -= self.STEP_SIZE
            if self.color_sensor.reflection() > self.THRESHOLD + 3:
                return True
        self.drivebase.turn(90)
        degrees = 0
        while degrees < 90:
            self.drivebase.turn(self.STEP_SIZE)
            degrees += self.STEP_SIZE

            if self.color_sensor.reflection() > self.THRESHOLD + 3:
                return True
        self.drivebase.turn(-90)
        return False

    def run(self):
        while Button.CENTER not in self.hub.buttons.pressed():
            if self.follow_line():
                break
