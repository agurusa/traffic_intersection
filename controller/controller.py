from .consts import NORTH, SOUTH, EAST, WEST, LEFT, STRAIGHT
from .lane import Lane

ORDER = (
    ((NORTH, SOUTH), LEFT),
    ((NORTH, SOUTH), STRAIGHT),
    ((EAST, WEST), LEFT),
    ((EAST, WEST), STRAIGHT)
)


class Controller:
    def __init__(self):
        self.lanes = [
            Lane((NORTH, SOUTH), LEFT),
            Lane((NORTH, SOUTH), STRAIGHT),
            Lane((EAST, WEST), LEFT),
            Lane((EAST, WEST), STRAIGHT)
        ]
        self.timer = 0
        self.current = None
