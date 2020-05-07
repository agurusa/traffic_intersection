NORTH = 'north'
SOUTH = 'south'
WEST = 'west'
EAST = 'east'

STRAIGHT = 'straight'
LEFT = 'left'

OFF = 0
ON = 1

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