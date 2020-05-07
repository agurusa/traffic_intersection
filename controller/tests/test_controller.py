import pytest
from controller import consts
from controller.controller import Controller


@pytest.fixture
def control():
    return Controller()


def test_controller_init(control):
    assert control.current_lane.direction == consts.ORDER[0]


def test_switch_lane(control):
    assert control.current_lane.light.state is consts.ON
    _prev = control.current_lane
    control.switch_lane()
    assert control.current_lane.light.state is consts.ON
    assert _prev.light.state is consts.OFF