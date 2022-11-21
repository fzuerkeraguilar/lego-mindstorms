from unitbricks import get_time

class MockData:
    def __init__(self, default_data = None):
        self._data = []
        self._default_data = None

    def get(self):
        if len(self._data) == 0:
            return self._default_data
        return self._data.pop(0)

    def add_point(self, point):
        self._data.append(point)

    def add_points(self, points):
        self._data.extend(points)

class TimedMockData:
    def __init__(self, default_data = None):
        self._data = []
        self._default_data = default_data

    def until(self, time, value):
        self._data.append((time, value))

    def get(self):
        current_time = get_time()
        if len(self._data) == 0:
            return self._default_data

        if current_time < self._data[0][0]:
            return self._data[0][1]
        else:
            self._data.pop(0)
            if len(self._data) == 0:
                return self._default_data
            else:
                return self._data[0][1]

class StaticMockData:
    def __init__(self, value):
        self._value = value

    def get():
        return self._value
