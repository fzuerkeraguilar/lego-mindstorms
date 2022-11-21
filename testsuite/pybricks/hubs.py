
class EV3Brick:
    def __init__(self):
        self.buttons = _Buttons()
        self.light = _Light()
        

class _Buttons:
    def __init__(self):
        self._mock_data = None

    def pressed(self):
        return self._mock_data.get()

    def _set_mock_data(self, data):
        self._mock_data = data

class _Light():
    def __init__(self):
        self._color = None

    def on(self, color):
        self._color = color

    def off(self):
        self._color = None

    def _get_status(self):
        return self._color
