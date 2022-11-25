from menu import Menu
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button
from unitbricks.mock import MockData
from unitbricks.assertion import assert_equals

def test_default_value():
    brick = EV3Brick()
    button_data = MockData()
    button_data.add_point([Button.RIGHT])
    brick.buttons._set(button_data)

    modes = [("Default", 42)]
    menu = Menu(brick, modes)
    result = menu.show()
    assert_equals(42, result)

def params_test_select_sequence():
    tests = []
    tests.append((
        3, [[Button.DOWN], [Button.DOWN], [Button.RIGHT]]
    ))
    tests.append((
        1, [[Button.DOWN], [Button.UP], [Button.RIGHT]]
    ))
    tests.append((
        2, [[Button.UP], [Button.UP], [Button.RIGHT]]
    ))
    tests.append((
        1, [[Button.DOWN], [Button.DOWN], [Button.DOWN], [Button.RIGHT]]
    ))
    tests.append((
        None, [[Button.LEFT]]
    ))
    return tests


def test_select_sequence(params):
    (expect, sequence) = params

    brick = EV3Brick()
    button_data = MockData()
    button_data.add_points(sequence)
    brick.buttons._set(button_data)

    modes = [("First", 1), ("Second", 2), ("Third", 3)]
    menu = Menu(brick, modes)
    result = menu.show()
    assert_equals(expect, result)

def test_arbitrary_data():
    brick = EV3Brick()
    button_data = MockData()
    button_data.add_points([[Button.RIGHT]])
    brick.buttons._set(button_data)

    modes = [("Default", brick)]
    menu = Menu(brick, modes)
    result = menu.show()
    assert_equals(brick, result)
