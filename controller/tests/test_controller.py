import pytest
from controller import consts
from controller.controller import Controller


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


# def test_run(control):
#     control.timer.time = 55  # test 5 seconds
#     _lanes = control._lanes
#     for lane in _lanes:  # put one car into each lane
#         lane.cars.put(1)
#

