from unitbricks import elapse, get_time

def wait(time):
    elapse(time)

class Stopwatch:
    def __init__(self):
        self._start_time = get_time()
        self._paused_at = None

    def reset(self):
        self._start_time = get_time()

    def pause(self):
        self._paused_at = get_time()

    def resume(self):
        self._paused_at = None

    def time(self):
        if self._paused_at == None:
            return get_time() - self._start_time
        else:
            return self._paused_at - self._start_time

class DataLog:
    def __init__(*headers, name='log', timestamp=True, extension='csv', append=False):
        pass

    def log(*values):
        pass
