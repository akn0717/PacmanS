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
        FPS = 15
        player = global_variables.PLAYERS[global_variables.PLAYER_ID]
        print(global_variables.CANVAS.board_data)
        assert isinstance(player, Pacman)
        while isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player.setDirection(Direction.UP.value)
                    elif event.key == pygame.K_DOWN:
                        player.setDirection(Direction.DOWN.value)
                    elif event.key == pygame.K_LEFT:
                        player.setDirection(Direction.LEFT.value)
                    elif event.key == pygame.K_RIGHT:
                        player.setDirection(Direction.RIGHT.value)

            # Clear display
            assert isinstance(global_variables.SCREEN_WINDOW, pygame.Surface)
            global_variables.SCREEN_WINDOW.fill(global_constants.PRIMARY_COLOR)

            # Update
            global_variables.CANVAS.update()

            # player will move every tick
            player.move(self.game_client)

            # Draw
            global_variables.CANVAS.draw()
            for player in global_variables.PLAYERS:
                player.draw()
            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()
