import pygame
import game.global_variables as global_variables
from game.global_constants import Block_Type


class Canvas:
    def __init__(self):
        self.board_data = None

    def update(self):
        # TODO: Handle recevie message from server and update the board state
        pass

    def draw(
        self,
    ):
        if self.board_data is None:
            return
        # Debug board
        # for i in range(self.size):
        #     for j in range(self.size):
        #         print(str(self.data[i, j]) + " ", end="")
        #     print()

        assert isinstance(global_variables.SCREEN_WINDOW, pygame.Surface)
        assert isinstance(global_variables.IMAGE_ASSET_EMPTY_BLOCK, pygame.Surface)
        assert isinstance(global_variables.IMAGE_ASSET_WALL_BLOCK, pygame.Surface)

        for i in range(self.board_data.shape[0]):
            for j in range(self.board_data.shape[1]):
                position = (
                    j * global_variables.CANVAS_UNIT[1],
                    i * global_variables.CANVAS_UNIT[0],
                )  # pygame display format is (column, row)
                if (
                    self.board_data[i][j] == Block_Type.EMPTY.value
                    or self.board_data[i][j] == Block_Type.DOT.value
                ):

                    global_variables.SCREEN_WINDOW.blit(
                        global_variables.IMAGE_ASSET_EMPTY_BLOCK,
                        position,
                    )
                elif self.board_data[i][j] == Block_Type.WALL.value:
                    global_variables.SCREEN_WINDOW.blit(
                        global_variables.IMAGE_ASSET_WALL_BLOCK,
                        position,
                    )

                if self.board_data[i][j] == Block_Type.DOT.value:
                    pass  # TODO: Load dot image and blit it here
