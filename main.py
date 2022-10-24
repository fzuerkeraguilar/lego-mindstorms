#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.ev3devices import Motor
from linefollower import LineFollower

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
right_motor = Motor(Port.B)
left_motor = Motor(Port.A)
# constant_motor = Motor(Port.C)
robot = DriveBase(left_motor, right_motor, wheel_diameter=33, axle_track=185)
color_sensor = ColorSensor(Port.S1)
touch_sensor = TouchSensor(Port.S2)

# Menu to select the program to run
ev3.screen.load_image(ImageFile.QUESTION_MARK)
ev3.speaker.beep()
# Wait for a button to be pressed
while not any(ev3.buttons.pressed()):
    wait(10)
    # Stop the program if the center button is pressed
    if Button.CENTER in ev3.buttons.pressed():
        ev3.speaker.beep()
        ev3.screen.print("Program stopped")
        wait(1000)
        ev3.screen.clear()
        break
    # Run the program if the left button is pressed
    elif Button.LEFT in ev3.buttons.pressed():
        ev3.speaker.beep()
        LineFollower(robot, color_sensor, touch_sensor).run()
    # Run the program if the right button is pressed
    elif Button.RIGHT in ev3.buttons.pressed():
      ev3.speaker.beep()
    #   constant_motor.run_time(1000, 100000, wait=True)
    # Run the program if the up button is pressed
    elif Button.UP in ev3.buttons.pressed():
        ev3.speaker.beep()
    # Run the program if the down button is pressed
    elif Button.DOWN in ev3.buttons.pressed():
        ev3.speaker.beep()

