class EV3Brick:
    def __init__(self):
        self.buttons = _Buttons()
        

class _Buttons:
    def __init__(self):
        self._pressed = []
    
    def set_pressed(self, pressed):
        self._pressed = pressed
    
    def pressed(self):
        return self._pressed