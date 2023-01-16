from multitouch_sensor import MultitouchSensor
from pybricks.ev3devices import TouchSensor
from unitbricks.mock import StaticMockData
from unitbricks.assertion import assert_equals, assert_more
from unitbricks import get_time

def test_general():
    sensor = MultitouchSensor(TouchSensor(None), TouchSensor(None))

def params_test_pressed():
    return [(True, True, True), (True, False, True), (False, True, True), (False, False, False)]

def test_pressed(params):
    left = TouchSensor(None)
    right = TouchSensor(None)

    (left_value, right_value, expected_value) = params
    left._set(StaticMockData(left_value))
    right._set(StaticMockData(right_value))

    sensor = MultitouchSensor(left, right)
    assert_equals(expected_value, sensor.pressed())


def params_test_pressed_left():
    return [(True, True, True), (True, False, True), (False, True, False), (False, False, False)]

def test_pressed_left(params):
    left = TouchSensor(None)
    right = TouchSensor(None)

    (left_value, right_value, expected_value) = params
    left._set(StaticMockData(left_value))
    right._set(StaticMockData(right_value))

    sensor = MultitouchSensor(left, right)
    assert_equals(expected_value, sensor.pressed_left())


def params_test_pressed_right():
    return [(True, True, True), (True, False, False), (False, True, True), (False, False, False)]

def test_pressed_right(params):
    left = TouchSensor(None)
    right = TouchSensor(None)

    (left_value, right_value, expected_value) = params
    left._set(StaticMockData(left_value))
    right._set(StaticMockData(right_value))

    sensor = MultitouchSensor(left, right)
    assert_equals(expected_value, sensor.pressed_right())