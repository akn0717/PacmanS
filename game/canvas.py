import pygame
import game.global_variables as global_variables
import game.global_constants as global_constants
from game.global_constants import Block_Type
import numpy as np


class Canvas:
    def __init__(self):
        self.board_data = None  # contains the whole board state, each cell is a value of the the global_constants.BLOCK_TYPE enum

    def update(self):
        pass  # client doesn't need to handle game logic so this is a stub function

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

        # assert if the variables are not in approriate types
        assert isinstance(global_variables.SCREEN_WINDOW, pygame.Surface)
        assert isinstance(global_variables.IMAGE_ASSET_EMPTY_BLOCK, pygame.Surface)
        assert isinstance(global_variables.IMAGE_ASSET_WALL_BLOCK, pygame.Surface)

        # draw board using board data, for each rows and column
        for i in range(self.board_data.shape[0]):
            for j in range(self.board_data.shape[1]):
                position = (
                    j * global_variables.CANVAS_UNIT[1]
                    + global_variables.BOARD_MARGIN,  # board_margin to plot the scores
                    i * global_variables.CANVAS_UNIT[0],
                )  # pygame display format is (column, row)
                # depending on block_type, different asset is drawn in cell
                if (
                    self.board_data[i][j] == Block_Type.EMPTY.value
                    or self.board_data[i][j] == Block_Type.DOT.value
                    or self.board_data[i][j] == Block_Type.BIG_DOT.value
                ):  # if it is a accessible block
                    global_variables.SCREEN_WINDOW.blit(
                        global_variables.IMAGE_ASSET_EMPTY_BLOCK,
                        position,
                    )
                elif self.board_data[i][j] == Block_Type.WALL.value:
                    global_variables.SCREEN_WINDOW.blit(
                        global_variables.IMAGE_ASSET_WALL_BLOCK,
                        position,
                    )

                # plotting on top of the accessible block
                if self.board_data[i][j] == Block_Type.DOT.value:
                    global_variables.SCREEN_WINDOW.blit(
                        global_variables.IMAGE_ASSET_DOT,
                        position,
                    )
                elif self.board_data[i][j] == Block_Type.BIG_DOT.value:
                    global_variables.SCREEN_WINDOW.blit(
                        global_variables.IMAGE_ASSET_BIG_DOT,
                        position,
                    )

    def score_display(self, players):
        max_score = max(
            [players[i].score for i in players]
        )  # the highest score is found to display crown

        # player 1 red top-left icon and score
        if 0 in players:
            score_text = global_variables.SCORE_FONT.render(
                f"Player {players[0].id + 1}: {players[0].score}",
                True,
                global_constants.COLORS[0],
            )

            # calculate where they should be shown
            text_width = score_text.get_width()
            text_height = score_text.get_height()
            text_margin = (global_variables.BOARD_MARGIN - text_width) / 2
            text_x = text_margin
            text_y = text_margin
            global_variables.SCREEN_WINDOW.blit(score_text, (text_x, text_y))

            icon_margin = (
                global_variables.BOARD_MARGIN - global_variables.ICON_PACMAN_SIZE
            ) / 2
            icon_x = icon_margin
            icon_y = text_y + global_variables.CANVAS_UNIT[1] * 2
            global_variables.SCREEN_WINDOW.blit(
                global_variables.SCORE_PLAYER_ASSETS[0], (icon_x, icon_y)
            )

            # Display clown for the pacman icon with highest score
            if players[0].score == max_score:
                global_variables.SCREEN_WINDOW.blit(
                    global_variables.ICON_CROWN,
                    (icon_x, icon_y - global_variables.ICON_PACMAN_SIZE / 4 * 3),
                )

        # player 2 green top-right icon and score
        if 1 in players:
            score_text = global_variables.SCORE_FONT.render(
                f"Player {players[1].id + 1}: {players[1].score}",
                True,
                global_constants.COLORS[1],
            )

            # calculate where they should be shown
            text_width = score_text.get_width()
            text_height = score_text.get_height()
            text_margin = (global_variables.BOARD_MARGIN - text_width) / 2
            text_x = global_variables.SCREEN_WIDTH - text_margin - text_width
            text_y = text_margin
            global_variables.SCREEN_WINDOW.blit(score_text, (text_x, text_y))
            icon_margin = (
                global_variables.BOARD_MARGIN - global_variables.ICON_PACMAN_SIZE
            ) / 2
            icon_x = (
                global_variables.SCREEN_WIDTH
                - icon_margin
                - global_variables.ICON_PACMAN_SIZE
            )
            icon_y = text_y + global_variables.CANVAS_UNIT[1] * 2
            global_variables.SCREEN_WINDOW.blit(
                global_variables.SCORE_PLAYER_ASSETS[1], (icon_x, icon_y)
            )

            # Display clown for the pacman icon with highest score
            if players[1].score == max_score:
                global_variables.SCREEN_WINDOW.blit(
                    global_variables.ICON_CROWN,
                    (icon_x, icon_y - global_variables.ICON_PACMAN_SIZE / 4 * 3),
                )

        # player 3 blue bottom left icon and score
        if 2 in players:
            score_text = global_variables.SCORE_FONT.render(
                f"Player {players[2].id + 1}: {players[2].score}",
                True,
                global_constants.COLORS[2],
            )

            # calculate where they should be shown
            text_width = score_text.get_width()
            text_height = score_text.get_height()
            text_margin = (global_variables.BOARD_MARGIN - text_width) / 2
            text_x = text_margin
            text_y = global_variables.SCREEN_HEIGHT - text_margin - text_height
            global_variables.SCREEN_WINDOW.blit(score_text, (text_x, text_y))
            icon_margin = (
                global_variables.BOARD_MARGIN - global_variables.ICON_PACMAN_SIZE
            ) / 2
            icon_x = icon_margin
            icon_y = text_y - icon_margin
            global_variables.SCREEN_WINDOW.blit(
                global_variables.SCORE_PLAYER_ASSETS[2], (icon_x, icon_y)
            )

            # Display clown for the pacman icon with highest score
            if players[2].score == max_score:
                global_variables.SCREEN_WINDOW.blit(
                    global_variables.ICON_CROWN,
                    (icon_x, icon_y - global_variables.ICON_PACMAN_SIZE / 4 * 3),
                )

        # player 4 yellow bottom right icon and score
        if 3 in players:
            score_text = global_variables.SCORE_FONT.render(
                f"Player {players[3].id + 1}: {players[3].score}",
                True,
                global_constants.COLORS[3],
            )

            # calculate where they should be shown
            text_width = score_text.get_width()
            text_height = score_text.get_height()
            text_margin = (global_variables.BOARD_MARGIN - text_width) / 2
            text_x = global_variables.SCREEN_WIDTH - text_margin - text_width
            text_y = global_variables.SCREEN_HEIGHT - text_margin - text_height
            global_variables.SCREEN_WINDOW.blit(score_text, (text_x, text_y))
            icon_margin = (
                global_variables.BOARD_MARGIN - global_variables.ICON_PACMAN_SIZE
            ) / 2
            icon_x = (
                global_variables.SCREEN_WIDTH
                - icon_margin
                - global_variables.ICON_PACMAN_SIZE
            )
            icon_y = text_y - icon_margin
            global_variables.SCREEN_WINDOW.blit(
                global_variables.SCORE_PLAYER_ASSETS[3], (icon_x, icon_y)
            )

            # Display clown for the pacman icon with highest score
            if players[3].score == max_score:
                global_variables.SCREEN_WINDOW.blit(
                    global_variables.ICON_CROWN,
                    (icon_x, icon_y - global_variables.ICON_PACMAN_SIZE / 4 * 3),
                )
