from pybricks.ev3devices import Motor
from pybricks.robotics import DriveBase
from unitbricks import get_time
from unitbricks.assertion import assert_equals, assert_less, assert_more

def create_drivebase(wheel_diameter, axle_track):
    left = Motor(None)
    right = Motor(None)
    drivebase = DriveBase(left, right, wheel_diameter, axle_track)
    return (drivebase, left, right)

def test_straight():
    (db, left, right) = create_drivebase(10, 10)
    db.settings(10, None, 10, None)

    assert_equals(0, left.angle())
    assert_equals(0, right.angle())
    assert_equals(0, get_time())

    db.straight(31)

    assert_less(360, left.angle())
    assert_more(355, left.angle())
    assert_less(360, right.angle())
    assert_more(355, right.angle())

    assert_less(36000, get_time())
    assert_more(35500, get_time())