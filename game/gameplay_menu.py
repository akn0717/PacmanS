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
    def __init__(self) -> None:
        super().__init__()

    def main(self):
        isRunning = True
        clock = pygame.time.Clock()
        FPS = 15

        while isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.players[self.player_id].setDirection(Direction.UP.value)
                    elif event.key == pygame.K_DOWN:
                        self.players[self.player_id].setDirection(Direction.DOWN.value)
                    elif event.key == pygame.K_LEFT:
                        self.players[self.player_id].setDirection(Direction.LEFT.value)
                    elif event.key == pygame.K_RIGHT:
                        self.players[self.player_id].setDirection(Direction.RIGHT.value)

            # Clear display
            assert isinstance(global_variables.SCREEN_WINDOW, pygame.Surface)
            global_variables.SCREEN_WINDOW.fill(global_constants.PRIMARY_COLOR)

            # Update
            self.canvas.update()

            # player will move every tick
            player = global_variables.PLAYERS[global_variables.PLAYER_ID]
            assert isinstance(player, Pacman)
            player.move()

            # Draw
            self.canvas.draw()
            for player in self.players:
                player.draw()
            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()
