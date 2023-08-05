# Size and associated UI components
global BOARD_WIDTH, BOARD_HEIGHT
global BOARD_MARGIN
global SCREEN_WIDTH, SCREEN_HEIGHT
global SCREEN_WINDOW
global CANVAS_UNIT

# image asset variables, we only load the images once at starting and store to these varaible so we don't need to reload it every time. they are loaded in the init() in main.py
global IMAGE_ASSET_EMPTY_BLOCK
global IMAGE_ASSET_WALL_BLOCK
global IMAGE_ASSET_DOT
global IMAGE_ASSET_BIG_DOT
global IMAGE_ASSET_PLAYERS

# used for in-game score display
global ICON_CROWN
global ICON_PACMAN_SIZE

# Shared memory between ui and tcp threads
global GAME_STARTED
global GAME_OVER
global QUIT_GAME
global DISCONNECTED_FROM_HOST
global PLAYER_ID
global PLAYERS
global CANVAS
global NUMBER_CONNECTIONS
global MOVING_REQUEST

# Shared memory mutex locks of the above shared memory
global MUTEX_PLAYERS  # a dictionary of locks for players
global MUTEX_PLAYERS_DICT  # a lock to lock the player dictionary

global MUTEX_CANVAS_CELLS  # a 2d array locks for cells
global MUTEX_CANVAS  # a single lock to lock the whole board data

## locking single variables
global MUTEX_MOVING_REQUEST
global MUTEX_PLAYER_ID
global GAME_STARTED_LOCK
global GAME_OVER_LOCK
global QUIT_GAME_LOCK
global DISCONNECTED_FROM_HOST_LOCK
