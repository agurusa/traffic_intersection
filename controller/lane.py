from . import light
from .consts import BOUNDS
import queue


class Lane:
    def __init__(self, direction):
        self._direction = direction
        self._maxtime = BOUNDS[direction][1]
        self._mintime = BOUNDS[direction][0]
        self._light = light.Light()
        self._cars = queue.Queue()
        self._sensor = self._cars.empty()

    @property
    def direction(self):
        return self._direction

    @property
    def light(self):
        return self._light

    @property
    def sensor(self):
        return not self._cars.empty()

    @property
    def maxtime(self):
        return self._maxtime

    @property
    def mintime(self):
        return self._mintime

    @property
    def cars(self):
        return self._cars

