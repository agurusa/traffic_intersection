from .consts import ORDER
from .lane import Lane
from .timer import Timer
from time import sleep

EXCEPT_NOCARS = 'no cars waiting anywhere'


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
    def next_lane(self):  # gets the next lane in order that has cars waiting
        cur_ind = self._lanes.index(self._current_lane)
        _next = _next_ind = cur_ind + 1 if cur_ind != len(self._lanes) - 1 else 0
        while _next_ind != cur_ind:  # find the next lane where a car is waiting
            if self.waiting(self._lanes[_next_ind]):
                return self._lanes[_next_ind]
            _next_ind = _next_ind + 1 if _next_ind != len(self._lanes) - 1 else 0
        return self._lanes[_next]  # if no lanes have cars, just return the next lane

    @property
    def timer(self):
        return self._timer

    def switch_lane(self):
        self.current_lane.light.switch_state()  # red light for current lane
        self._current_lane = self.next_lane  # update state
        self._timer.restart()

    def waiting(self, _lane):  # tells you if cars are waiting in a lane
        return True if _lane.sensor else False

    def noone_waiting(self):
        for lane in self._lanes:
            if self.waiting(lane):
                return False
        return True

    def run(self):  # main controller logic
        while True:
            while self.noone_waiting() and self.timer.time < self.current_lane.mintime:
                self.timer.time += 1
                sleep(1)

            while self.current_lane.sensor and self.timer.time < self.current_lane.maxtime:
                self.timer.time += 1
                sleep(1)

            self.switch_lane()
