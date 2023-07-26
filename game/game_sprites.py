import game.global_constants as global_constants
import game.global_variables as global_variables
import pygame
import numpy as np
from game.global_constants import Direction, Move_Operation, Message_Type


class Pacman:
    def __init__(self, id, name=""):
        self.id = id
        self.position = (0, 0)
        self.name = name
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
        game_client.sendDataToServer(
            Message_Type.REQUEST_PLAYER_MOVE,
            [self.id, *new_position],
        )

    def update(self):
        # Client thread will update the self.position, so nothing is determined here yet
        pass

    def draw(self):
        position = (
            self.position[1] * global_variables.CANVAS_UNIT[1],
            self.position[0] * global_variables.CANVAS_UNIT[0],
        )  # pygame display format is (column, row)
        global_variables.SCREEN_WINDOW.blit(self.image_asset, position)
