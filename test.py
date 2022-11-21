#!./test
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button

brick = EV3Brick()
assert not Button.LEFT in brick.buttons.pressed()
brick.buttons.set_pressed([Button.LEFT, Button.RIGHT])
assert Button.LEFT in brick.buttons.pressed()