import numpy as np
from enum import Enum

CANVAS_SIZE = (20, 20)
PRIMARY_COLOR = (100, 100, 100)
BLOCK_SIZE = (100, 100)

NUM_PLAYERS = 4


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 3
    DOWN = 2


class Move_Operation(Enum):
    OPERATOR_RIGHT = (0, 1)
    OPERATOR_LEFT = (0, -1)
    OPERATOR_DOWN = (1, 0)
    OPERATOR_UP = (-1, 0)
    OPERATORS = [
        OPERATOR_RIGHT,
        OPERATOR_LEFT,
        OPERATOR_DOWN,
        OPERATOR_UP,
    ]


class Block_Type(Enum):
    EMPTY = 0
    WALL = 1
    DOT = 2


class Message_Type(Enum):
    INITIAL_BOARD = 0
    PLAYER_POSITION = 1
    PLAYER_SCORE = 2
