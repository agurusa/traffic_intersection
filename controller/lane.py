from . import light, sensor
from .consts import BOUNDS


class Lane:
    def __init__(self, direction):
        self._direction = direction
        self._maxtime = BOUNDS[direction][1]
        self._mintime = BOUNDS[direction][0]
        self._light = light.Light()
        self._sensor = sensor.Sensor()

    @property
    def direction(self):
        return self._direction

    @property
    def light(self):
        return self._light

    @property
    def sensor(self):
        return self._sensor

    @property
    def maxtime(self):
        return self._maxtime

    @property
    def mintime(self):
        return self._mintime

