import numpy as np
from game.global_variables import CANVAS_SIZE
import pygame
import game.global_variables as global_variables


class Canvas:
    def __init__(self, board_data):
        self.__board_data = board_data

        self.players = []  # player positions
        self.__score_data = np.zeros_like(self.__board_data)

        self.asset_empty_block = pygame.image.load("../assets/EmptyBlock.png")
        self.asset_block = pygame.image.load("../assets/Block.png")
        num_players = 4
        # TODO get player ids from the server and assign them with each image color
        self.asset_players = [
            pygame.image.load("../assets/PacmanYellow.png")
            .convert_alpha()
            .set_colorkey(((255, 255, 255) / num_players) * i)
            for i in range(num_players)
        ]

    def __blockType(self, i, j):
        code = 0
        if i - 1 >= 0:
            code |= self.data[i - 1][j] == 1
        if i + 1 < self.size:
            code |= (self.data[i + 1][j] == 1) << 1
        if j - 1 >= 0:
            code |= (self.data[i][j - 1] == 1) << 2
        if j + 1 < self.size:
            code |= (self.data[i][j + 1] == 1) << 3
        return code

    def draw(
        self,
    ):
        # Debug board
        # for i in range(self.size):
        #     for j in range(self.size):
        #         print(str(self.data[i, j]) + " ", end="")
        #     print()

        assert isinstance(global_variables.SCREEN_WINDOW, pygame.Surface)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.__board_data[i][j] == 0 or self.__board_data[i][j] == 2:
                    global_variables.SCREEN_WINDOW.blit(
                        self.asset_empty_block,
                        (i, j) * self.asset_empty_block.get_size[0],
                    )
                elif self.__board_data[i][j] == 1:
                    global_variables.SCREEN_WINDOW.blit(
                        self.asset_block,
                        (i, j) * self.asset_block.get_size[0],
                    )

                if self.__board_data[i][j] == 2:
                    pass  # TODO: Load dot image and blit it here

        for i in range(len(self.players)):
            global_variables.SCREEN_WINDOW.blit(self.asset_players[i], self.players[i])
