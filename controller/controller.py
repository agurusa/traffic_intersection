from .consts import NORTH, SOUTH, EAST, WEST, LEFT, STRAIGHT, ORDER
from .lane import Lane


class Controller:
    def __init__(self):
        self._lanes = [Lane(direction) for direction in ORDER]
        self._timer = 0
        self._current_lane = self._lanes[0]

    @property
    def current_lane(self):
        return self._current_lane
