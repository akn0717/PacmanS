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
        self.position += global_constants.MOVE_DIRECTIONS[self.direction]
        

        # TODO: send message to server to request for a move here

    def update(self):
        # Client thread will update the self.position, so nothing is determined here yet
        pass

    def draw(self):
        global_variables.SCREEN_WINDOW.blit(self.image_asset, self.position)
