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
