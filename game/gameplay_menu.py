from game.menu import Menu
from game.canvas import Canvas
import numpy as np
import pygame

# Debug
from network.GameServer import GameServer


class Gameplay_Menu(Menu):
    def __init__(self, host: str = None) -> None:
        super().__init__()
        # TODO: receive board data from server and pass it to Canvas()

        # workaround for initilize game board
        gameServer = GameServer()
        gameServer.initializeGameData()

        self.canvas = Canvas(np.zeros)

    def main(self):
        isRunning = True
        while isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = True
                elif event.type == pygame.K_UP:
                    pass
                elif event.type == pygame.K_DOWN:
                    pass
                elif event.type == pygame.K_LEFT:
                    pass
                elif event.type == pygame.K_RIGHT:
                    pass

            self.canvas.update()
            self.canvas.draw()
