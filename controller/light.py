from .consts import OFF, ON

class Light:
    def __init__(self):
        self._state = OFF

    @property
    def state(self):
        return self._state

    def switch_state(self):
        self._state = OFF if self._state else ON
