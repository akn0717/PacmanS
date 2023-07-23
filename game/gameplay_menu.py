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

# Debug
from network.Game_Server import GameServer


class Gameplay_Menu(Menu):
    def __init__(self) -> None:
        super().__init__()
        # TODO: receive board data from server and pass it to Canvas()

        # workaround for initilize game board
        # gameServer = GameServer(5555)
        # gameServer.initializeGameData()
        self.canvas = Canvas()

        # TODO: Move this to the room menu
        global_variables.MUTEX_CANVAS_CELLS = [
            [Lock() for j in range(global_constants.CANVAS_SIZE[1])]
            for i in range(global_constants.CANVAS_SIZE[0])
        ]
        ######################################

        gameClient = Game_Client()
        self.players = [
            Pacman(i, gameServer.players[i])
            for i in range(global_constants.NUM_PLAYERS)
        ]  # player positions
        gameClient.connect("127.0.0.1", 5555)

        self.canvas.board_data

        self.player_id = (
            0  # For Debuging only, TODO: receive player_id from server message
        )

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

            # For game testing only, skipping exchanging message,
            # remove later when the network is ready
            player = self.players[self.player_id]
            (i, j) = player.position
            if (
                player.direction == Direction.RIGHT.value
                and j < global_constants.CANVAS_SIZE[1] - 1
                and self.canvas.board_data[i][j + 1] == Block_Type.EMPTY.value
            ):
                player.move()
            elif (
                player.direction == Direction.LEFT.value
                and j > 0
                and self.canvas.board_data[i][j - 1] == Block_Type.EMPTY.value
            ):
                player.move()
            elif (
                player.direction == Direction.DOWN.value
                and i < global_constants.CANVAS_SIZE[1] - 1
                and self.canvas.board_data[i + 1][j] == Block_Type.EMPTY.value
            ):
                player.move()
            elif (
                player.direction == Direction.UP.value
                and i > 0
                and self.canvas.board_data[i - 1][j] == Block_Type.EMPTY.value
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
