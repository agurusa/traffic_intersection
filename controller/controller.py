from .consts import NORTH, SOUTH, EAST, WEST, LEFT, STRAIGHT, ORDER
from .lane import Lane


class Controller:
    def __init__(self):
        self._lanes = [Lane(direction) for direction in ORDER]
        self._timer = 0
        # start with N,S,Turning lane with a green light
        self._current_lane = self._lanes[0]
        self._current_lane.light.switch_state()

    @property
    def current_lane(self):
        return self._current_lane

    @property
    def timer(self):
        return self._timer

    def switch_lane(self):
        self.current_lane.light.switch_state()  # red light for current lane
        cur_ind = self._lanes.index(self._current_lane)
        next_ind = cur_ind + 1 if cur_ind != len(self._lanes) - 1 else 0
        self._current_lane = self._lanes[next_ind]
        self.current_lane.light.switch_state()  # green light for next lane
