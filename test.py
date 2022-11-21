#!./test
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button, Color
from unitbricks.mock import MockData

brick = EV3Brick()
button_mock = MockData()
button_mock.add_point([Button.CENTER])
button_mock.add_point([Button.LEFT, Button.RIGHT])

brick.buttons._set_mock_data(button_mock)

assert not Button.LEFT in brick.buttons.pressed()
assert Button.LEFT in brick.buttons.pressed()

assert brick.light._get_status() == None
brick.light.on(Color.RED)
assert brick.light._get_status() == Color.RED
