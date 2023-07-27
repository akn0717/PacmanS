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
        FPS = 10
        while isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].setDirection(Direction.UP.value)
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].movingRequest = False
                    elif event.key == pygame.K_DOWN:
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].setDirection(Direction.DOWN.value)
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].movingRequest = False
                    elif event.key == pygame.K_LEFT:
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].setDirection(Direction.LEFT.value)
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].movingRequest = False
                    elif event.key == pygame.K_RIGHT:
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].setDirection(Direction.RIGHT.value)
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].movingRequest = False

            # Clear display
            assert isinstance(global_variables.SCREEN_WINDOW, pygame.Surface)
            global_variables.SCREEN_WINDOW.fill(global_constants.PRIMARY_COLOR)

            # Update
            global_variables.CANVAS.update()
            # player will move every tick

            with global_variables.MUTEX_PLAYERS[global_variables.PLAYER_ID]:
                if (
                    global_variables.PLAYERS[global_variables.PLAYER_ID].movingRequest
                    == False
                ):
                    global_variables.PLAYERS[global_variables.PLAYER_ID].move(
                        self.game_client
                    )

            # Draw
            global_variables.CANVAS.draw()
            for id in range(len(global_variables.PLAYERS)):
                player = global_variables.PLAYERS[id]
                if player.id == id:
                    player.draw()
            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()
