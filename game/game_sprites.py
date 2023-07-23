import game.global_constants as global_constants
import game.global_variables as global_variables


class Pacman:
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.score = 0
        self.image_asset = global_constants.IMAGE_ASSET_PLAYERS[id]
        self.direction = 0

    def setDirection(self, direction):
        self.direction = direction

    def __move(self, i, j):

        # For game testing only, skipping exchanging message, remove later when the network is ready
        self.position = (i, j)

        # TODO: send message to server to request for a move here
        pass

    def update(self):
        (i, j) = self.position
        if self.direction == 0:
            self.__move(i, j + 1)
        elif self.direction == 1:
            self.__move(i, j - 1)
        elif self.direction == 2:
            self.__move(i + 1, j)
        elif self.direction == 3:
            self.__move(i - 1, j)

    def draw(self):
        global_variables.SCREEN_WINDOW.blit(self.image_asset, self.position)
