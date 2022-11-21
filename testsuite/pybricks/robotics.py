import math
from unitbricks import elapse

class DriveBase:
    def __init__(self, left_motor, right_motor, wheel_diameter, axle_track):
        self._left_motor = left_motor
        self._right_motor = right_motor
        self._wheel_diameter = wheel_diameter
        self._axle_track = axle_track
        self._straight_speed = 0
        self._turn_rate = 0

    def settings(self, straight_speed, straight_acceleration, turn_rate, turn_acceleration):
        # NOTE: acceleration not supported by mock
        self._straight_speed = straight_speed
        self._turn_rate = turn_rate

    def straight(self, distance):
        wheel_length = self._wheel_diameter * math.pi
        angle = distance * 360 / wheel_length
        time = abs((angle / self._straight_speed) * 1000)
        self._left_motor.run(self._straight_speed)
        self._right_motor.run(self._straight_speed)
        elapse(time)

    def turn(self, angle):
        #distance = angle * self._axle_track * math.pi / 360
        #wheel_length = self._wheel_diameter * math.pi
        #wheel_angle = distance * 360 / wheel_length
        wheel_angle = angle * self._axle_track / self._wheel_diameter
        time = abs(self.turn_rate / angle)

        dist_per_deg = self._axle_track * math.pi / 360
        distance = angle * dist_per_deg
        # TODO

    def drive(self, drive_speed, turn_rate):
        # TODO
        pass

    def stop():
        self._left_motor.stop()
        self._right_motor.stop()

    def distance():
        return 0 # TODO

    def angle():
        return 0 # TODO

    def state():
        return (self.distance(), self._straight_speed, self.angle(), self._turn_rate)

    def reset():
        # TODO
        pass