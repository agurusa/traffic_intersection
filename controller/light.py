OFF = 0
ON = 1


class Light:
    def __init__(self):
        self._state = OFF

    @property
    def state(self):
        return self._state
