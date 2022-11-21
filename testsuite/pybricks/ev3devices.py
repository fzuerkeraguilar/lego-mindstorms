from unitbricks.mock import MockData

class TouchSensor:
    def __init__(self):
        self._data = None

    def _set(self, data = MockData(False)):
        self._data = data

    def pressed(self):
        return self._data.get()

class UltrasonicSensor:
    def __init__(self):
        self._data = None

    def _set(self, data = MockData(0)):
        self._data = data

    def distance(self, silent=False):
        return self._data.get()

class GyroSensor():
    pass

class InfraredSensor():
    pass

class ColorSensor():
    pass

class Motor():
    pass
