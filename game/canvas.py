import pygame
import game.global_variables as global_variables
import game.global_constants as global_constants
import numpy as np


class Canvas:
    def __init__(self, board_data):
        self.board_data = board_data

    def update(self):
        # TODO: Handle recevie message from server and update the board state
        pass

    def draw(
        self,
    ):
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
                    i * global_variables.CANVAS_UNIT[0],
                    j * global_variables.CANVAS_UNIT[1],
                )
                if self.board_data[i][j] == 0 or self.board_data[i][j] == 2:
                    global_variables.SCREEN_WINDOW.blit(
                        global_variables.IMAGE_ASSET_EMPTY_BLOCK,
                        position,
                    )
                elif self.board_data[i][j] == 1:
                    global_variables.SCREEN_WINDOW.blit(
                        global_variables.IMAGE_ASSET_WALL_BLOCK,
                        position,
                    )

                if self.board_data[i][j] == 2:
                    pass  # TODO: Load dot image and blit it here
