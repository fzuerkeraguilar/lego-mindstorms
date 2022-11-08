#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Button
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import ImageFile

from linefollower import LineFollower
from debug import Debug
from turning_distance_sensor import TurningDistanceSensor


ev3 = EV3Brick()
right_motor = Motor(Port.B)
left_motor = Motor(Port.A)
distance_drive = Motor(Port.C)
drive_base = DriveBase(left_motor, right_motor, wheel_diameter=33, axle_track=185)
color_sensor = ColorSensor(Port.S1)
r_touch_sensor = TouchSensor(Port.S2)
l_touch_sensor = TouchSensor(Port.S3)
distance_sensor = TurningDistanceSensor(Port.C, Port.S4)

# Menu to select the program to run
ev3.screen.load_image(ImageFile.QUESTION_MARK)
ev3.speaker.beep()
# Wait for a button to be pressed
while not any(ev3.buttons.pressed()):
    wait(10)
    if Button.CENTER in ev3.buttons.pressed():
        ev3.speaker.beep()
        Debug(drive_base, color_sensor, r_touch_sensor, distance_sensor, ev3, right_motor, left_motor, distance_drive, 100).run()
        break

    elif Button.UP in ev3.buttons.pressed():
        ev3.speaker.beep()
        LineFollower(drive_base, right_motor, left_motor, color_sensor, r_touch_sensor, distance_sensor, ev3).run()
        break

    elif Button.RIGHT in ev3.buttons.pressed():
        ev3.speaker.beep()
        break

    elif Button.DOWN in ev3.buttons.pressed():
        ev3.speaker.beep()
        break

    elif Button.LEFT in ev3.buttons.pressed():
        ev3.speaker.beep()
        break

