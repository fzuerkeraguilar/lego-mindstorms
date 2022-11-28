from pybricks.ev3devices import Motor
from pybricks.robotics import DriveBase
from unitbricks import get_time, elapse
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

    assert_equals(3100, get_time())
    assert_equals(left.angle(), right.angle())

    assert_equals(31, db.distance())


def test_turn():
    (db, left, right) = create_drivebase(10, 10)
    db.settings(10, None, 90, None)  # 90 deg/s and 10mm/s

    assert_equals(0, left.angle())
    assert_equals(0, right.angle())
    assert_equals(0, get_time())

    db.turn(180)
    assert_equals(2 * 1000, get_time())
    assert_equals(left.angle(), -right.angle())
    assert_more(0, left.angle())

    assert_equals(180, db.angle())


def test_reset():
    (db, left, right) = create_drivebase(10, 10)
    db.settings(10, None, 90, None)  # 90 deg/s and 10mm/s

    assert_equals(0, db.distance())
    assert_equals(0, db.angle())

    db.straight(10)
    db.turn(20)
    assert_equals(10, db.distance())
    assert_equals(20, db.angle())

    db.straight(5)
    db.turn(5)
    assert_equals(15, db.distance())
    assert_equals(25, db.angle())

    db.reset()
    assert_equals(0, db.distance())
    assert_equals(0, db.angle())


def test_manual_straight():
    (db, left, right) = create_drivebase(10, 10)
    db.settings(10, None, 90, None)  # 90 deg/s and 10mm/s

    db.drive(10, 0)
    elapse(0.5 * 1000)
    (dist, speed, angle, turn_rate) = db.state()
    assert_equals(5, dist)
    assert_equals(10, speed)
    assert_equals(0, angle)
    assert_equals(0, turn_rate)

    elapse(0.5 * 1000)
    assert_equals(10, db.distance())
    assert_equals(0, db.angle())

    db.stop()
    (dist, speed, angle, turn_rate) = db.state()
    assert_equals(10, dist)
    assert_equals(0, speed)
    assert_equals(0, angle)
    assert_equals(0, turn_rate)


def test_manual_turn():
    (db, left, right) = create_drivebase(10, 10)
    db.settings(10, None, 90, None)  # 90 deg/s and 10mm/s

    db.drive(0, 90)
    elapse(0.5 * 1000)
    (dist, speed, angle, turn_rate) = db.state()
    assert_equals(0, dist)
    assert_equals(0, speed)
    assert_equals(45, angle)
    assert_equals(90, turn_rate)

    elapse(0.5 * 1000)
    assert_equals(0, db.distance())
    assert_equals(90, db.angle())

    db.stop()
    (dist, speed, angle, turn_rate) = db.state()
    assert_equals(0, dist)
    assert_equals(0, speed)
    assert_equals(90, angle)
    assert_equals(0, turn_rate)


def test_auto_manual():
    (db, left, right) = create_drivebase(10, 10)
    db.settings(10, None, 90, None)  # 90 deg/s and 10mm/s

    db.drive(10, 90)
    assert_equals(0, db.distance())
    assert_equals(0, db.angle())

    elapse(1 * 1000)
    assert_equals(10, db.distance())
    assert_equals(90, db.angle())
    db.stop()

    db.turn(-180)
    assert_equals(3 * 1000, get_time())
    assert_equals(10, db.distance())
    assert_equals(-90, db.angle())

    db.straight(-20)
    assert_equals(5 * 1000, get_time())
    assert_equals(-10, db.distance())
    assert_equals(-90, db.angle())

    db.drive(20, 180)
    assert_equals(5 * 1000, get_time())
    assert_equals(-10, db.distance())
    assert_equals(-90, db.angle())

    elapse(1 * 1000)
    assert_equals(6 * 1000, get_time())
    assert_equals(10, db.distance())
    assert_equals(90, db.angle())

    db.stop()
    elapse(1 * 1000)
    assert_equals(7 * 1000, get_time())
    assert_equals(10, db.distance())
    assert_equals(90, db.angle())

    db.reset()
    assert_equals(0, db.distance())
    assert_equals(0, db.angle())
