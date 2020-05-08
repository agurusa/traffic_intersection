class Timer():
    def __init__(self):
        self._time = 0

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, t):
        self._time = t

    def restart(self):
        self._time = 0