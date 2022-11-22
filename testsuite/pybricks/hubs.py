from unitbricks.mock import MockData

class EV3Brick:
    def __init__(self):
        self.buttons = _Buttons()
        self.light = _Light()
        self.screen = _Screen()
        

class _Buttons:
    def __init__(self):
        self._mock_data = None

    def pressed(self):
        if self._mock_data == None:
            return []
        return self._mock_data.get()

    def _set(self, data = MockData([])):
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
class _Screen:
    def __init__(self):
        pass

    def print(self, *args, sep='', end='\n'):
        print(*args, sep=sep, end=end)

    def clear(self):
        pass
