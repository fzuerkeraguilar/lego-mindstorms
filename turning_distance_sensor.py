from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait

class TurningDistanceSensor:

    def __init__(self, motor_port, ultrasonic_sensor_port, speed=100):
        self.turn_motor = Motor(motor_port)
        self.ultrasonic_sensor = UltrasonicSensor(ultrasonic_sensor_port)
        self.speed = speed
        self.turn_motor.reset_angle(0)

    def set_angle(self, angle):
        if angle > 90 or angle < -90:
            raise ValueError("Angle must be between -90 and 90 degrees")
        self.turn_motor.run_angle(self.speed, angle, wait=True)

    def measure_angle(self, angle):
        if angle > 90 or angle < -90:
            raise ValueError("Angle must be between -90 and 90 degrees")
        self.turn_motor.run_angle(self.speed, angle, wait=True)
        distance = self.ultrasonic_sensor.distance()
        self.turn_motor.run_angle(self.speed, -angle, wait=True)
        return distance

    def run_target(self, target_angle, wait=True):
        self.turn_motor.run_target(self.speed, target_angle, wait=wait)
    
    def run_angle(self, angle, wait=True):
        self.turn_motor.run_angle(self.speed, angle, wait=wait)

    def distance(self):
        return self.ultrasonic_sensor.distance()