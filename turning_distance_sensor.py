from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait


class TurningDistanceSensor:
    def __init__(self, turn_motor, ultrasonic_sensor, speed=100):
        self.turn_motor = turn_motor
        self.ultrasonic_sensor = ultrasonic_sensor
        self.speed = speed
        self.turn_motor.run_until_stalled(-100, Stop.BRAKE)
        wait(500)
        self.turn_motor.reset_angle(0)

    def set_angle(self, angle, wait=True):
        if angle > 90 or angle < -90:
            raise ValueError("Angle must be between -90 and 90 degrees")
        self.turn_motor.run_target(self.speed, angle, then=Stop.HOLD, wait=wait)

    def set_up(self):
        self.turn_motor.run_until_stalled(100, then=Stop.HOLD)

    def set_up_soft(self):
        self.turn_motor.run_until_stalled(100, then=Stop.BRAKE)

    def set_down(self):
        self.turn_motor.run_until_stalled(-100, then=Stop.HOLD)
        self.turn_motor.reset_angle(0)

    def set_down_soft(self):
        self.turn_motor.run_until_stalled(-100, then=Stop.BRAKE)

    def measure_angle(self, angle):
        if angle > 90 or angle < -90:
            raise ValueError("Angle must be between -90 and 90 degrees")
        self.turn_motor.run_target(self.speed, angle, wait=True)
        distance = self.ultrasonic_sensor.distance()
        self.turn_motor.run_target(self.speed, 0, wait=True)
        return distance

    def run_target(self, target_angle, wait=True):
        self.turn_motor.run_target(self.speed, target_angle, wait=wait)

    def run_angle(self, angle, wait=True):
        self.turn_motor.run_angle(self.speed, angle, wait=wait)

    def distance(self):
        return self.ultrasonic_sensor.distance()
