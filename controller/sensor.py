class Sensor:
    def __init__(self):
        self._car = False

    @property
    def car(self):
        return self._car
