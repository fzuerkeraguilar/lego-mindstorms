import math
from unitbricks import elapse, get_time


class DriveBase:
    def __init__(self, left_motor, right_motor, wheel_diameter, axle_track):
        self._left_motor = left_motor
        self._right_motor = right_motor
        self._wheel_diameter = wheel_diameter
        self._axle_track = axle_track
        self._straight_speed = 0
        self._turn_rate = 0
        self._current_speed = None
        self._current_turn_rate = None
        self._start_time = None
        self._distance = 0
        self._angle = 0

    def _auto_mode(self):
        self._distance = self.distance()
        self._angle = self.angle()
        self._current_speed = None
        self._current_turn_rate = None
        self._start_time = None

    def settings(
        self, straight_speed, straight_acceleration, turn_rate, turn_acceleration
    ):
        # NOTE: acceleration not supported by mock
        self._straight_speed = straight_speed
        self._turn_rate = turn_rate

    def straight(self, distance):
        if self._start_time != None:
            raise ValueError("DriveBase is in manual mose. Exit with .stop()")
        self._auto_mode()
        wheel_length = self._wheel_diameter * math.pi
        angle = distance * 360 / wheel_length
        time = abs(distance / self._straight_speed) * 1000
        wheel_speed = angle / time

        self._left_motor.run(wheel_speed)
        self._right_motor.run(wheel_speed)

        self._distance = self._distance + distance
        elapse(time)

    def turn(self, angle):
        if self._start_time != None:
            raise ValueError("DriveBase is in manual mose. Exit with .stop()")
        self._auto_mode()
        time = abs((angle / self._turn_rate) * 1000)
        length_per_deg = self._axle_track * math.pi / 360
        speed = length_per_deg * self._turn_rate
        if angle < 0:
            speed = -speed

        self._left_motor.run(speed)
        self._right_motor.run(-speed)

        self._angle = self._angle + angle
        elapse(time)

    def drive(self, drive_speed, turn_rate):
        self._auto_mode()  # to store driven distance and angle
        self._start_time = get_time()
        self._current_speed = drive_speed
        self._current_turn_rate = turn_rate

    def stop(self):
        self._auto_mode()
        self._left_motor.stop()
        self._right_motor.stop()

    def distance(self):
        if self._current_speed != None:
            return (
                self._distance
                + self._current_speed * (get_time() - self._start_time) / 1000
            )
        else:
            return self._distance  # TODO: manual mode distance

    def angle(self):
        if self._current_turn_rate != None:
            return (
                self._angle
                + self._current_turn_rate * (get_time() - self._start_time) / 1000
            )
        else:
            return self._angle  # TODO: manual mode distance

    def state(self):
        speed = 0
        turn_rate = 0
        if self._current_speed != None:
            speed = self._current_speed
        if self._current_turn_rate != None:
            turn_rate = self._current_turn_rate
        return (self.distance(), speed, self.angle(), turn_rate)

    def reset(self):
        self._distance = 0
        self._angle = 0
