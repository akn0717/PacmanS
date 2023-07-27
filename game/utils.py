from game.global_constants import Block_Type


def isValidMove(board_data, new_position):
    if (
        new_position[0] < 0
        or new_position[0] >= board_data.shape[0]
        or new_position[1] < 0
        or new_position[1] >= board_data.shape[1]
    ):
        return False

    # if board_data[new_position[0]][new_position[1]] == Block_Type.WALL.value:
    #     return False

    return True
