import numpy as np
from enum import Enum

CANVAS_SIZE = (20, 20)
PRIMARY_COLOR = (119, 136, 153)
BLOCK_SIZE = (100, 100)

COLORS = [
    (255, 200, 0),  # yellow
    (255, 0, 0),  # red
    (0, 128, 0),  # green
    (0, 0, 255),  # blue
]

NUM_PLAYERS = 4

NUM_DEFAULT_COMMUNICATION_BYTES = 512


class Direction(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


class Move_Operation(Enum):
    OPERATOR_RIGHT = (0, 1)
    OPERATOR_UP = (-1, 0)
    OPERATOR_LEFT = (0, -1)
    OPERATOR_DOWN = (1, 0)

    OPERATORS = [
        OPERATOR_RIGHT,
        OPERATOR_UP,
        OPERATOR_LEFT,
        OPERATOR_DOWN,
    ]


class Block_Type(Enum):
    EMPTY = 0
    WALL = 1
    DOT = 2
    BIG_DOT = 3


class Message_Type(Enum):
    INITIAL_BOARD = 0
    PLAYER_POSITION = 1
    PLAYER_SCORE = 2
    REQUEST_PLAYER_MOVE = 3
    PLAYER_JOIN = 4
    UPDATE_BLOCK = 5
    HOST_GAME_STARTED = 6
    PLAYER_ID = 7
    PLAYER_DISCONNECT = 8
    GAME_OVER = 9
