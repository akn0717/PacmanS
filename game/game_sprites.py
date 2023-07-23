import game.global_constants as global_constants
import game.global_variables as global_variables
import pygame
import numpy as np


class Pacman:
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.score = 0
        isinstance(global_variables.IMAGE_ASSET_PLAYERS[id], pygame.Surface)
        self.image_asset = global_variables.IMAGE_ASSET_PLAYERS[id]
        self.direction = 0

    def setDirection(self, direction):
        self.direction = direction

    def move(self):
        # For game testing only, skipping exchanging message,
        # remove later when the network is ready
        self.position += global_constants.MOVE_DIRECTIONS[self.direction]

        # TODO: send message to server to request for a move here

    def update(self):
        # Client thread will update the self.position, so nothing is determined here yet
        pass

    def draw(self):
        position = (
            self.position[1] * global_variables.CANVAS_UNIT[1],
            self.position[0] * global_variables.CANVAS_UNIT[0],
        )  # pygame display format is (column, row)
        global_variables.SCREEN_WINDOW.blit(self.image_asset, position)
