class Button:
    LEFT_DOWN = 1
    LEFT_MINUS = 2
    DOWN = 3
    RIGHT_DOWN = 4
    RIGHT_MINUS = 5
    LEFT = 6
    CENTER = 7
    RIGHT = 8
    LEFT_UP = 9
    LEFT_PLUS = 10
    UP = 11
    BEACON = 12
    RIGHT_UP = 13
    RIGHT_PLUS = 14

class Port:
    A = 1
    B = 2
    C = 3
    D = 4
    S1 = 10
    S2 = 11
    S3 = 12
    S4 = 13

class Direction:
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2

class Stop:
    COAST = 1
    BRAKE = 2
    HOLD = 3

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    BLACK = 1 #Self(0, 0, 0)
    # BLUE = Self(0, 0, 100)
    # GREEN = Self(0, 100, 0)
    # YELLOW = Self(100, 100, 0)
    RED = 2 #Self(100, 0, 0)
    # WHITE = Self(100, 100, 100)
    # BROWN = Self(50, 50, 50)
    # ORANGE = Self(100, 50, 50)
    # PURPLE = Self(100, 0, 100)
