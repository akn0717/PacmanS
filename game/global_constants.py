import numpy as np

CANVAS_SIZE = (20, 20)
PRIMARY_COLOR = (100, 100, 100)
BLOCK_SIZE = (100, 100)
MOVE_DIRECTIONS = [
    np.asarray((0, 1)),
    np.asarray((0, -1)),
    np.asarray((1, 0)),
    np.asarray((-1, 0)),
]
NUM_PLAYERS = 4
