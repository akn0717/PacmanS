import game.global_variables as global_variables
import pygame
import numpy as np
from game.global_constants import Direction, Move_Operation, Message_Type
from game.utils import isValidMove
from network.utils import concatBuffer


class Pacman:
    def __init__(self, id, position=(0, 0)):
        # initialize pacman with id, position, score and icon.
        self.id = id
        self.position = position
        self.score = 0
        isinstance(global_variables.IMAGE_ASSET_PLAYERS[int(id)], pygame.Surface)
        image_asset = global_variables.IMAGE_ASSET_PLAYERS[int(id)]
        self.image_assets = [
            # transform the pacman to make the mouth pointing to different directions
            pygame.transform.rotate(image_asset, 90.0 * direction)
            for direction in range(4)
        ]
        self.direction = Direction.RIGHT.value

    def setDirection(self, direction):
        self.direction = direction

    def move(self, game_client):
        # calculate new position of pacman according to input
        new_position = self.position + np.array(
            Move_Operation.OPERATORS.value[self.direction]
        )
        new_position = (int(new_position[0]), int(new_position[1]))
        # preliminary check to see if move is valid and has no obstacle
        if not (isValidMove(global_variables.CANVAS.board_data, new_position)):
            return
        # if move valid send request to server for taking that position
        args = [self.id, *new_position]
        args = [str(arg) for arg in args]
        message = concatBuffer(
            Message_Type.REQUEST_PLAYER_MOVE.value,
            args,
        )
        game_client.sendDataToServer(message)

    def update(self):
        # Client thread will update the self.position, so no movement logic is implemented here
        pass

    # draw the Pacman asset in current position on the board
    def draw(self):
        position = (
            self.position[1] * global_variables.CANVAS_UNIT[1]
            + global_variables.BOARD_MARGIN,
            self.position[0] * global_variables.CANVAS_UNIT[0],
        )  # pygame display format is (column, row)
        global_variables.SCREEN_WINDOW.blit(self.image_assets[self.direction], position)
