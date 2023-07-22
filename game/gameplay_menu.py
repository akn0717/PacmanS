from game.menu import Menu
from game.canvas import Canvas
import pygame


class Gameplay_Menu(Menu):
    def __init__(self, host: str = None) -> None:
        super().__init__()
        if (
            host is not None
        ):  # is a client, TODO: recieve and init the game board based on the game board from host
            pass
        else:  # is a server, responsible for generating the game board
            self.canvas = Canvas()

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
