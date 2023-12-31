from enum import Enum

# maximum number of players the game can handle
MAX_NUM_PLAYERS = 4

# the size of the game board
CANVAS_SIZE = (20, 20)

# primary color theme for the whole game
PRIMARY_COLOR = (119, 136, 153)

# color for each PACMAN
COLORS = [
    (255, 200, 0),  # yellow
    (255, 0, 0),  # red
    (0, 128, 0),  # green
    (0, 0, 255),  # blue
]


# number of maximum bytes each time send and receive using TCP socket
NUM_DEFAULT_COMMUNICATION_BYTES = 512


# enums for movement logics
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


# enums for block types
class Block_Type(Enum):
    EMPTY = 0
    WALL = 1
    DOT = 2
    BIG_DOT = 3


# enums for message type used in network communication
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
