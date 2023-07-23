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

    def move(self):
        # For game testing only, skipping exchanging message, remove later when the network is ready
        (i, j) = self.position
        if self.direction == 0 and j < global_constants.CANVAS_SIZE[1] - 1:
            self.position = (i, j + 1)
        elif self.direction == 1 and j > 0:
            self.position = (i, j - 1)
        elif self.direction == 2 and i < global_constants.CANVAS_SIZE[1] - 1:
            self.position = (i + 1, j)
        elif self.direction == 3 and i > 0:
            self.position = (i - 1, j)

        # TODO: send message to server to request for a move here

    def update(self):
        # Client thread will update the self.position, so nothing is determined here yet
        pass

    def draw(self):
        global_variables.SCREEN_WINDOW.blit(self.image_asset, self.position)
