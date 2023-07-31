from multiprocessing import Lock
from game.game_sprites import Pacman
from game.menu import Menu
from game.canvas import Canvas
import numpy as np
import pygame
import game.global_constants as global_constants
import game.global_variables as global_variables
from game.global_constants import Direction, Block_Type
from network.Game_Client import Game_Client


class Gameplay_Menu(Menu):
    def __init__(self, game_client) -> None:
        super().__init__()
        self.game_client = game_client

    def main(self):
        isRunning = True
        clock = pygame.time.Clock()
        FPS = 60
        updateIteration = 0
        while isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                    self.game_client.close_socket()
                    # pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].setDirection(Direction.UP.value)
                    elif event.key == pygame.K_DOWN:
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].setDirection(Direction.DOWN.value)
                    elif event.key == pygame.K_LEFT:
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].setDirection(Direction.LEFT.value)
                    elif event.key == pygame.K_RIGHT:
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].setDirection(Direction.RIGHT.value)

            # Clear display
            assert isinstance(global_variables.SCREEN_WINDOW, pygame.Surface)
            global_variables.SCREEN_WINDOW.fill(global_constants.PRIMARY_COLOR)

            # Update
            global_variables.CANVAS.update()
            # player will move every tick

            if updateIteration % 20 == 0:
                global_variables.MOVING_REQUEST = False

            with global_variables.MUTEX_MOVING_REQUEST:
                if global_variables.MOVING_REQUEST == False:
                    with global_variables.MUTEX_PLAYERS[global_variables.PLAYER_ID]:
                        global_variables.PLAYERS[global_variables.PLAYER_ID].move(
                            self.game_client
                        )

            updateIteration += 1
            # Draw
            global_variables.CANVAS.draw()
            for player_id in global_variables.PLAYERS:
                global_variables.PLAYERS[player_id].draw()

            global_variables.CANVAS.score_display(global_variables.PLAYERS)

            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()
