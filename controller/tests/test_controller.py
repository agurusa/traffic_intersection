import pytest
from controller import consts
from controller.controller import Controller
import threading
import datetime as dt
from time import sleep


@pytest.fixture
def control():
    return Controller()


def test_controller_init(control):
    assert control.current_lane.direction == consts.ORDER[0]


def test_next_lane(control):
    assert control.next_lane.direction == consts.ORDER[1]


def test_switch_lane(control):
    assert control.current_lane.light.state is consts.ON
    _prev = control.current_lane
    control.switch_lane()
    assert control.current_lane.light.state is consts.ON
    assert _prev.light.state is consts.OFF
    assert control.timer.time == 0


def test_waiting(control):
    assert control.waiting() is False
    control.next_lane.cars.put(1)
    assert control.waiting() is True


def test_run(control):
    for lane in control._lanes:  # put one car into each lane
        lane.cars.put(1)
        
    now = dt.datetime.now()
    end = now + dt.timedelta(0, 5)  # test for 5 seconds
    green_lanes = set()
    lock = threading.Lock()
    intersection = threading.Thread(target=control.run, daemon=True)
    intersection.start()
    while now < end:
        # move traffic
        with lock:
            if not control.current_lane.cars.empty():
                control.current_lane.cars.get()
            _current_lane = control.current_lane
            sleep(0.25)
        green_lanes.add(_current_lane.direction)
        now = dt.datetime.now()
    assert green_lanes == set(consts.ORDER)
