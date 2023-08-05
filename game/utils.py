from game.global_constants import Block_Type

# check if a move is valid based on boundaries and the type of the target block
# return True if it is moveable, otherwise False
def isValidMove(board_data, new_position):
    if (
        new_position[0] < 0
        or new_position[0] >= board_data.shape[0]
        or new_position[1] < 0
        or new_position[1] >= board_data.shape[1]
    ):
        return False

    if board_data[new_position[0]][new_position[1]] == Block_Type.WALL.value:
        return False

    return True
