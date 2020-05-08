NORTH = 'north'
SOUTH = 'south'
WEST = 'west'
EAST = 'east'

STRAIGHT = 'straight'
LEFT = 'left'

OFF = 'RED'
ON = 'GREEN'

ORDER = (
    ((NORTH, SOUTH), LEFT),
    ((NORTH, SOUTH), STRAIGHT),
    ((EAST, WEST), LEFT),
    ((EAST, WEST), STRAIGHT)
)

# in seconds
BOUNDS = {
    ((NORTH, SOUTH), LEFT): [10, 60],
    ((NORTH, SOUTH), STRAIGHT): [30, 120],
    ((EAST, WEST), LEFT): [10, 30],
    ((EAST, WEST), STRAIGHT): [30, 60],
}

# cars move in/out of intersection at 4 Hz
CAR_SPEED = 0.25