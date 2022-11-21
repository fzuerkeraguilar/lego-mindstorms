from unitbricks.mock import StaticMockData
from pybricks.parameters import Direction, Stop
from unitbricks import get_time, elapse

class TouchSensor:
    def __init__(self, port):
        self._data = StaticMockData(False)

    def _set(self, data):
        self._data = data

    def pressed(self):
        return self._data.get()

class UltrasonicSensor:
    def __init__(self, port):
        self._data = StaticMockData(0)

    def _set(self, data):
        self._data = data

    def distance(self, silent=False):
        return self._data.get()

class GyroSensor():
    def __init__(self, port):
        pass

class InfraredSensor():
    def __init__(self, port):
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
    def __init__(self, positive_direction=Direction.CLOCKWISE, gears=None):
        self._current_speed = 0 # deg/s
        self._start_time = get_time()
        self._prev_angle = 0 # cummulated previous angle
        self._reset_angle = 0
        self._duration = None # only for run_time
        self._rotation_angle = None # only for run_angle
        self._rewind = False # only for negative run_angle

    def _current_angle(self):
        duration = (get_time() - self._start_time) / 1000
        if self._duration != None:
            if duration * 1000 > self._duration:
                duration = self._duration / 1000

        angle_increase = self._current_speed * duration
        if self._rotation_angle != None:
            if not self._rewind and angle_increase > self._rotation_angle:
                angle_increase = self._rotation_angle
            elif self._rewind and angle_increase < -self._rotation_angle:
                angle_increase = -self._rotation_angle

        return self._prev_angle + angle_increase

    def _cumulate_angle(self):
        self._prev_angle = self._current_angle()

    def speed(self): 
        if self._duration != None:
            if get_time() >= self._start_time + self._duration:
                return 0

        if self._rotation_angle != None:
            if not self._rewind and self._current_angle() >= self._rotation_angle + self._prev_angle:
                return 0
            elif self._rewind and self._current_angle() <= -self._rotation_angle + self._prev_angle:
                return 0

        return self._current_speed

    def angle(self): 
        return self._current_angle() - self._reset_angle
        
    def reset_angle(self, angle): 
        self._reset_angle = self._current_angle()

    def stop(self): # improvement: cruising
        self._cumulate_angle()
        self._start_time = get_time()
        self._current_speed = 0
        
    def brake(self):
        self.stop()

    def hold(self): 
        self.stop()

    def run(self, speed): 
        self._cumulate_angle()
        self._start_time = get_time()
        self._current_speed = speed
        self._duration = None
        self._rotation_angle = None
        self._rewind = False

    def run_time(self, speed, time, then=Stop.HOLD, wait=True):
        self._cumulate_angle()
        self._start_time = get_time()
        self._current_speed = speed
        self._duration = time
        self._rotation_angle = None
        self._rewind = False
        if wait == True:
            elapse(time)

    def run_angle(self, speed, rotation_angle, then=Stop.HOLD, wait=True): 
        self._rewind = rotation_angle < 0
        if rotation_angle < 0:
            rotation_angle = -rotation_angle
            speed = -speed
        self._cumulate_angle()
        self._start_time = get_time()
        self._current_speed = speed
        self._duration = None
        self._rotation_angle = rotation_angle
        if wait == True:
            time = abs((rotation_angle / speed) * 1000)
            elapse(time)

    def run_target(self, speed, target_angle, then=Stop.HOLD, wait=True): 
        angle_distance = target_angle - self._current_angle()
        self.run_angle(speed, angle_distance, then, wait)

    def run_until_stalled(self, speed, then=Stop.COAST, duty_limit=None): 
        pass

    def dc(self, duty): pass
    def track_target(self, target_angle): pass
