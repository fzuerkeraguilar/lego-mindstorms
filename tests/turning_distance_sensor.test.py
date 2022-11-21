from turning_distance_sensor import TurningDistanceSensor
from pybricks.parameters import Port, Button
from pybricks.ev3devices import (Motor, UltrasonicSensor)
from unitbricks.mock import StaticMockData
from unitbricks.assertion import assert_equals, assert_more
from unitbricks import get_time

def test_general():
    sensor = TurningDistanceSensor(Motor(None), UltrasonicSensor(None))



def params_test_invalid_angle():
    return [100, -100, 91, -91]

def test_invalid_angle(angle):
    try:
        sensor = TurningDistanceSensor(Motor(None), UltrasonicSensor(None))
        sensor.set_angle(angle)
        return False
    except ValueError:
        return True



def params_test_valid_angle():
    return [0, 70, -70, 90, -90]

def test_valid_angle(angle):
    sensor = TurningDistanceSensor(Motor(None), UltrasonicSensor(None))
    sensor.set_angle(angle)



def params_test_distance():
    return [0, 100, 55, 200]

def test_distance(expected):
    distance_data = StaticMockData(expected)
    ultraSensor = UltrasonicSensor(Port.S4)
    ultraSensor._set(distance_data)
    sensor = TurningDistanceSensor(Motor(None), ultraSensor)
    distance = sensor.distance()
    assert_equals(expected, distance)



def params_test_measure_angle():
    return [(90, 10), (0, 5), (-90, 200)]

def test_measure_angle(expected):
    (e_angle, e_distance) = expected
    distance_data = StaticMockData(e_distance)
    motor = Motor(None)
    ultraSensor = UltrasonicSensor(None)
    ultraSensor._set(distance_data)
    sensor = TurningDistanceSensor(motor, ultraSensor)
    distance = sensor.measure_angle(e_angle)
    angle = motor.angle()
    assert_equals(e_distance, distance, "Sensor distance data")
    assert_equals(0, angle, "Sensor angle") # sensor is turned back afterwards
    if e_angle != 0:
        assert_more(0, get_time())



def params_test_set_angle():
    return (90, 70, 0, -80, -90)

def test_set_angle(expected):
    motor = Motor(None)
    sensor = TurningDistanceSensor(motor, UltrasonicSensor(None))

    assert_equals(0, motor.angle())
    sensor.set_angle(expected)
    assert_equals(expected, motor.angle())

