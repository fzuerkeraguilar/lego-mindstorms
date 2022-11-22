from turning_distance_sensor import TurningDistanceSensor
from pybricks.parameters import Port, Button
from pybricks.ev3devices import (Motor, UltrasonicSensor)
from unitbricks.mock import StaticMockData
from unitbricks.assertion import assert_equals
from unitbricks import elapse, get_time

def test_motor():
    motor = Motor(None)
    assert_equals(0, motor.speed())
    assert_equals(0, motor.angle())

def test_reset_angle():
    motor = Motor(None)
    assert_equals(0, motor.angle())

    motor.run(10)
    elapse(1 * 1000)
    assert_equals(10, motor.angle())

    motor.run(20)
    elapse(0.5 * 1000)
    assert_equals(20, motor.angle())

    motor.reset_angle(0)
    assert_equals(0, motor.angle())

    motor.run(10)
    elapse(1 * 1000)
    assert_equals(10, motor.angle())

def test_stop():
    motor = Motor(None)
    assert_equals(0, motor.speed())
    assert_equals(0, motor.angle())

    motor.run(10)
    elapse(1 * 1000)
    assert_equals(10, motor.angle())
    assert_equals(10, motor.speed())

    motor.stop()
    elapse(1 * 1000)
    assert_equals(0, motor.speed())
    assert_equals(10, motor.angle())

    motor.run(10)
    elapse(1 * 1000)
    assert_equals(20, motor.angle())
    assert_equals(10, motor.speed())

def test_run_time():
    motor = Motor(None)
    assert_equals(0, motor.speed())
    assert_equals(0, motor.angle())

    motor.run_time(10, 1 * 1000, wait=False)
    assert_equals(10, motor.speed())
    assert_equals(0, motor.angle())
    assert_equals(0, get_time())

    elapse(2 * 1000)
    assert_equals(10, motor.angle())
    assert_equals(0, motor.speed())
    assert_equals(2 * 1000, get_time())

    motor.run_time(20, 1 * 1000, wait=True)
    assert_equals(0, motor.speed())
    assert_equals(3 * 1000, get_time())
    assert_equals(30, motor.angle())

def test_run_angle():
    motor = Motor(None)
    assert_equals(0, motor.speed())
    assert_equals(0, motor.angle())

    motor.run_angle(10, 10, wait=False)
    assert_equals(10, motor.speed())
    assert_equals(0, motor.angle())
    assert_equals(0, get_time())

    elapse(2 * 1000)
    assert_equals(0, motor.speed())
    assert_equals(10, motor.angle())
    assert_equals(2 * 1000, get_time())

    motor.run_angle(10, 10, wait=True)
    assert_equals(3 * 1000, get_time())
    assert_equals(0, motor.speed())
    assert_equals(20, motor.angle())

def test_run_negative():
    motor = Motor(None)
    assert_equals(0, motor.speed())
    assert_equals(0, motor.angle())

    motor.run(-10)
    assert_equals(-10, motor.speed())
    assert_equals(0, motor.angle())

    elapse(1 * 1000)
    assert_equals(-10, motor.speed())
    assert_equals(-10, motor.angle())
    
    motor.run(10)
    assert_equals(10, motor.speed())
    assert_equals(-10, motor.angle())

    elapse(1 * 1000)
    assert_equals(10, motor.speed())
    assert_equals(0, motor.angle())

def test_run_time_negative():
    motor = Motor(None)
    assert_equals(0, motor.speed())
    assert_equals(0, motor.angle())

    motor.run_time(-10, 1 * 1000, wait=False)
    assert_equals(-10, motor.speed())
    assert_equals(0, motor.angle())

    elapse(2 * 1000)
    assert_equals(0, motor.speed())
    assert_equals(-10, motor.angle())

    motor.run_time(-10, 1 * 1000, wait=True)
    assert_equals(0, motor.speed())
    assert_equals(-20, motor.angle())

def test_run_angle_negative():
    motor = Motor(None)
    assert_equals(0, motor.speed())
    assert_equals(0, motor.angle())

    motor.run_angle(10, -10, wait=False)
    assert_equals(-10, motor.speed())
    assert_equals(0, motor.angle())

    elapse(2 * 1000)
    assert_equals(0, motor.speed())
    assert_equals(-10, motor.angle())
    assert_equals(2 * 1000, get_time())

    motor.run_angle(20, -10, wait=True)
    assert_equals(0, motor.speed())
    assert_equals(-20, motor.angle())
    assert_equals(2.5 * 1000, get_time())

def test_run_target():
    motor = Motor(None)
    assert_equals(0, motor.speed())
    assert_equals(0, motor.angle())

    motor.run_target(10, 10, wait=False)
    assert_equals(10, motor.speed())
    assert_equals(0, motor.angle())

    elapse(2 * 1000)
    assert_equals(0, motor.speed())
    assert_equals(10, motor.angle())
    assert_equals(2 * 1000, get_time())

    motor.run_target(10, 20, wait=True)
    assert_equals(0, motor.speed())
    assert_equals(20, motor.angle())
    assert_equals(3 * 1000, get_time())

    motor.run_target(30, -10, wait=True)
    assert_equals(0, motor.speed())
    assert_equals(-10, motor.angle())
    assert_equals(4 * 1000, get_time())