from game.game_sprites import Pacman
from game.menu import Menu
from game.canvas import Canvas
import numpy as np
import pygame
import game.global_constants as global_constants

# Debug
from network.GameServer import GameServer


class Gameplay_Menu(Menu):
    def __init__(self, host: str = None) -> None:
        super().__init__()
        # TODO: receive board data from server and pass it to Canvas()

        # workaround for initilize game board
        gameServer = GameServer()
        gameServer.initializeGameData()

        self.canvas = Canvas(gameServer.board_data)
        self.players = [Pacman(i, (0, 0)) for i in range(4)]  # player positions
        self.player_id = (
            0  # For Debuging only, TODO: receive player_id from server message
        )

    def main(self):
        isRunning = True
        while isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = True
                elif event.type == pygame.K_UP:
                    self.players[self.player_id].setDirection(3)
                elif event.type == pygame.K_DOWN:
                    self.players[self.player_id].setDirection(2)
                elif event.type == pygame.K_LEFT:
                    self.players[self.player_id].setDirection(1)
                elif event.type == pygame.K_RIGHT:
                    self.players[self.player_id].setDirection(0)

            # Update
            self.canvas.update()

            # player will move every tick
            self.players[self.player_id].move()

            # Draw
            self.canvas.draw()
            for player in self.players:
                player.draw()
