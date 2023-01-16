class MultitouchSensor:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def pressed(self):
        return self.left.pressed() or self.right.pressed()

    def pressed_left(self):
        return self.left.pressed()

    def pressed_right(self):
        return self.right.pressed()