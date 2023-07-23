import pygame
from game.game_sprites import Pacman
import game.global_variables as global_variables
import game.global_constants as global_constants


class Canvas:
    def __init__(self, board_data):
        self.__board_data = board_data

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
        for i in range(self.__board_data.shape[0]):
            for j in range(self.__board_data.shape[1]):
                if self.__board_data[i][j] == 0 or self.__board_data[i][j] == 2:
                    global_variables.SCREEN_WINDOW.blit(
                        global_constants.IMAGE_ASSET_EMPTY_BLOCK,
                        (i, j) * global_constants.IMAGE_ASSET_EMPTY_BLOCK.get_size[0],
                    )
                elif self.__board_data[i][j] == 1:
                    global_variables.SCREEN_WINDOW.blit(
                        global_constants.IMAGE_ASSET_WALL_BLOCK,
                        (i, j) * global_constants.IMAGE_ASSET_WALL_BLOCK.get_size[0],
                    )

                if self.__board_data[i][j] == 2:
                    pass  # TODO: Load dot image and blit it here
