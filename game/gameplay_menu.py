from game.game_sprites import Pacman
from game.menu import Menu
from game.canvas import Canvas
import numpy as np
import pygame
import game.global_constants as global_constants
import game.global_variables as global_variables

# Debug
from network.GameServer import GameServer


class Gameplay_Menu(Menu):
    def __init__(self, host: str = None) -> None:
        super().__init__()
        # TODO: receive board data from server and pass it to Canvas()

        # workaround for initilize game board
        gameServer = GameServer(5555)
        gameServer.initializeGameData()

        self.canvas = Canvas(gameServer.board_data)
        self.players = [
            Pacman(i, gameServer.players[i])
            for i in range(global_constants.NUM_PLAYERS)
        ]  # player positions
        self.player_id = (
            0  # For Debuging only, TODO: receive player_id from server message
        )

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
                        self.players[self.player_id].setDirection(3)
                    elif event.key == pygame.K_DOWN:
                        self.players[self.player_id].setDirection(2)
                    elif event.key == pygame.K_LEFT:
                        self.players[self.player_id].setDirection(1)
                    elif event.key == pygame.K_RIGHT:
                        self.players[self.player_id].setDirection(0)

            # Clear display
            assert isinstance(global_variables.SCREEN_WINDOW, pygame.Surface)
            global_variables.SCREEN_WINDOW.fill(global_constants.PRIMARY_COLOR)

            # Update
            self.canvas.update()

            # player will move every tick

            # For game testing only, skipping exchanging message, remove later when the network is ready
            player = self.players[self.player_id]
            (i, j) = player.position
            if (
                player.direction == 0
                and j < global_constants.CANVAS_SIZE[1] - 1
                and self.canvas.board_data[i][j + 1] == 0
            ):
                player.move()
            elif (
                player.direction == 1
                and j > 0
                and self.canvas.board_data[i][j - 1] == 0
            ):
                player.move()
            elif (
                player.direction == 2
                and i < global_constants.CANVAS_SIZE[1] - 1
                and self.canvas.board_data[i + 1][j] == 0
            ):
                player.move()
            elif (
                player.direction == 3
                and i > 0
                and self.canvas.board_data[i - 1][j] == 0
            ):
                player.move()
            ################################################################################################

            # Draw
            self.canvas.draw()
            for player in self.players:
                player.draw()
            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()
