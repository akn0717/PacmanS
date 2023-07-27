import game.global_constants as global_constants
import game.global_variables as global_variables
import pygame
import numpy as np
from game.global_constants import Direction, Move_Operation, Message_Type
from game.utils import isValidMove
from network.utils import concatBuffer


class Pacman:
    def __init__(self, id, name="", position=(0, 0)):
        self.id = id
        self.position = position
        self.name = name
        self.movingRequest = True
        self.score = 0
        isinstance(global_variables.IMAGE_ASSET_PLAYERS[int(id)], pygame.Surface)
        self.image_asset = global_variables.IMAGE_ASSET_PLAYERS[int(id)]
        self.direction = Direction.RIGHT.value

    def setDirection(self, direction):
        self.direction = direction

    def move(self, game_client):
        # For game testing only, skipping exchanging message,
        # remove later when the network is ready
        new_position = self.position + np.array(
            Move_Operation.OPERATORS.value[self.direction]
        )
        new_position = (int(new_position[0]), int(new_position[1]))
        self.movingRequest = True

        if not (isValidMove(global_variables.CANVAS.board_data, new_position)):
            return
        print(type(new_position))
        print("Client sends new position", new_position)
        args = [self.id, *new_position]
        args = [str(arg) for arg in args]
        message = concatBuffer(
            Message_Type.REQUEST_PLAYER_MOVE.value,
            args,
        )
        game_client.sendDataToServer(message)

    def update(self):
        # Client thread will update the self.position, so nothing is determined here yet
        pass

    def draw(self):
        position = (
            self.position[1] * global_variables.CANVAS_UNIT[1],
            self.position[0] * global_variables.CANVAS_UNIT[0],
        )  # pygame display format is (column, row)
        global_variables.SCREEN_WINDOW.blit(self.image_asset, position)
