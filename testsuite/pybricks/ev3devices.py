from unitbricks.mock import StaticMockData

class TouchSensor:
    def __init__(self):
        self._data = StaticMockData(False)

    def _set(self, data):
        self._data = data

    def pressed(self):
        return self._data.get()

class UltrasonicSensor:
    def __init__(self):
        self._data = StaticMockData(0)

    def _set(self, data):
        self._data = data

    def distance(self, silent=False):
        return self._data.get()

class GyroSensor():
    pass

class InfraredSensor():
    pass

class ColorSensor():
    def __init__(self, port):
        self._ambient_data = StaticMockData(0)
        self._reflection_data = StaticMockData(0)
        self._rgb_data = StaticMockData(0)

    def ambient(self):
        return self._ambient_data.get()

    def reflection(self):
        return self._reflection_data.get()

    def rgb(self):
        return self._rgb_data.get()

    def _set_ambient(self, data):
        self._ambient_data = data

    def _set_reflection(self, data):
        self._reflection_data = data

    def _set_rgb(self, data):
        self._rgb_data = data

    pass

class Motor():
    pass
