from . import light, sensor
from .consts import NORTH, SOUTH, EAST, WEST, LEFT, STRAIGHT

# in seconds
BOUNDS = {
    ((NORTH, SOUTH), LEFT): [10, 60],
    ((NORTH, SOUTH), STRAIGHT): [30, 120],
    ((EAST, WEST), LEFT): [10, 30],
    ((EAST, WEST), STRAIGHT): [30, 60],
}


class Lane:
    def __init__(self, coming, going):
        self._maxtime = BOUNDS[self._direction[1]]
        self._mintime = BOUNDS[self._direction][0]
        self._direction = (coming, going)
        self._light = light.Light()
        self._sensor = sensor.Sensor()

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

