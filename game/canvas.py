import pygame
import game.global_variables as global_variables
import game.global_constants as global_constants
from game.global_constants import Block_Type
import numpy as np


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
                    j * global_variables.CANVAS_UNIT[1] + global_variables.BOARD_MARGIN,
                    # j * global_variables.CANVAS_UNIT[1],
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
    
    

    def score_display(self, players):
        scores = [players[0].score, 
                  players[1].score, 
                  players[2].score, 
                  players[3].score]
        
        for i in range(4):
            
            if i == 0:          # player 1 red top-left
                score_text = global_variables.SCORE_FONT.render(
                    f"Player {players[i].id + 1}: {scores[i]}", 
                    True, 
                    global_constants.COLORS[i]
                )
                text_width = score_text.get_width()
                text_height = score_text.get_height()
                text_margin = (
                    global_variables.BOARD_MARGIN - 
                    text_width
                    ) / 2
                text_x = text_margin
                text_y = text_margin
                global_variables.SCREEN_WINDOW.blit(
                    score_text, 
                    (text_x, text_y)
                )

                icon_margin = (
                    global_variables.BOARD_MARGIN - 
                    global_variables.ICON_PACMAN_SIZE
                    ) / 2
                icon_x = icon_margin
                icon_y = text_y + global_variables.CANVAS_UNIT[1] * 2
                global_variables.SCREEN_WINDOW.blit(
                    global_variables.ICON_PACMAN_RED, 
                    (icon_x, icon_y)
                )

                # Display clown for the pacman icon with highest score
                if scores[i] == max(scores):
                    global_variables.SCREEN_WINDOW.blit(
                        global_variables.ICON_CROWN, 
                        (icon_x, icon_y - global_variables.ICON_PACMAN_SIZE / 4 * 3)
                    )
                i += 1

            elif i == 1:        # player 2 green top-right
                if global_variables.NUMBER_CONNECTIONS < 2:
                    continue

                score_text = global_variables.SCORE_FONT.render(
                    f"Player {players[i].id + 1}: {scores[i]}", 
                    True, 
                    global_constants.COLORS[i]
                )
                text_width = score_text.get_width()
                text_height = score_text.get_height()
                text_x = global_variables.SCREEN_WIDTH - text_margin - text_width
                global_variables.SCREEN_WINDOW.blit(score_text, (text_x, text_y))

                icon_x = global_variables.SCREEN_WIDTH - icon_margin - global_variables.ICON_PACMAN_SIZE
                global_variables.SCREEN_WINDOW.blit(
                    global_variables.ICON_PACMAN_GREEN, 
                    (icon_x, icon_y)
                )

                # Display clown for the pacman icon with highest score
                if scores[i] == max(scores):
                    global_variables.SCREEN_WINDOW.blit(
                        global_variables.ICON_CROWN, 
                        (icon_x, icon_y - global_variables.ICON_PACMAN_SIZE / 4 * 3)
                    )
                i += 1

            elif i == 2:        # player 3 blue bottom left
                if global_variables.NUMBER_CONNECTIONS < 3:
                    continue

                score_text = global_variables.SCORE_FONT.render(
                    f"Player {players[i].id + 1}: {scores[i]}", 
                    True, 
                    global_constants.COLORS[i]
                )
                text_width = score_text.get_width()
                text_height = score_text.get_height()
                text_x = text_margin
                text_y = global_variables.SCREEN_HEIGHT - text_margin - text_height
                global_variables.SCREEN_WINDOW.blit(
                    score_text, 
                    (text_x, text_y)
                )

                icon_x = icon_margin
                icon_y = text_y - icon_margin
                global_variables.SCREEN_WINDOW.blit(
                    global_variables.ICON_PACMAN_BLUE, 
                    (icon_x, icon_y)
                )

                # Display clown for the pacman icon with highest score
                if scores[i] == max(scores):
                    global_variables.SCREEN_WINDOW.blit(
                        global_variables.ICON_CROWN, 
                        (icon_x, icon_y - global_variables.ICON_PACMAN_SIZE / 4 * 3)
                    )
                i += 1   

            else:               # player 4 yellow bottom right
                if global_variables.NUMBER_CONNECTIONS < 4:
                    continue

                score_text = global_variables.SCORE_FONT.render(
                    f"Player {players[i].id + 1}: {scores[i]}", 
                    True, 
                    global_constants.COLORS[i]
                )
                text_width = score_text.get_width()
                text_height = score_text.get_height()
                text_x = global_variables.SCREEN_WIDTH - text_margin - text_width
                global_variables.SCREEN_WINDOW.blit(score_text, (text_x, text_y))
                
                icon_x = global_variables.SCREEN_WIDTH - icon_margin - global_variables.ICON_PACMAN_SIZE
                global_variables.SCREEN_WINDOW.blit(
                    global_variables.ICON_PACMAN_YELLOW, 
                    (icon_x, icon_y)
                )

                # Display clown for the pacman icon with highest score
                if scores[i] == max(scores):
                    global_variables.SCREEN_WINDOW.blit(
                        global_variables.ICON_CROWN, 
                        (icon_x, icon_y - global_variables.ICON_PACMAN_SIZE / 4 * 3)
                    )
                i += 1
                
            