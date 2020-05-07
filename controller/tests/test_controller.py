import pytest
from controller import consts
from controller.controller import Controller


@pytest.fixture
def control():
    return Controller()


def test_controller_init(control):
    assert control.current_lane.direction == consts.ORDER[0]
