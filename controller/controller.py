from .consts import ORDER
from .lane import Lane
from .timer import Timer
from time import sleep


class Controller:
    def __init__(self):
        self._lanes = [Lane(direction) for direction in ORDER]
        self._timer = Timer()
        # start with N,S,Turning lane with a green light
        self._current_lane = self._lanes[0]
        self._current_lane.light.switch_state()
        self._next_lane = self._lanes[1]

    @property
    def current_lane(self):
        return self._current_lane

    @property
    def next_lane(self):  # gets the next lane in order
        cur_ind = self._lanes.index(self._current_lane)
        _next_ind = cur_ind + 1 if cur_ind != len(self._lanes) - 1 else 0
        return self._lanes[_next_ind]

    @property
    def timer(self):
        return self._timer

    def switch_lane(self):
        self.current_lane.light.switch_state()  # red light for current lane
        self._current_lane = self.next_lane  # update state
        self.current_lane.light.switch_state()  # green light for new current lane
        self._timer.restart()

    def waiting(self):  # tells you if cars are waiting in the next lane
        return True if self.next_lane.sensor else False

    def run(self):  # main controller logic
        while True:
            while not (self.waiting() and self.timer.time > self.current_lane.maxtime) and self.current_lane.sensor:
                self.timer.time += 1
                sleep(1)
            self.switch_lane()
