import game.global_constants as global_constants
import game.global_variables as global_variables


class Pacman:
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.score = 0
        self.image_asset = global_constants.IMAGE_ASSET_PLAYERS[id]

    def update(self):
        pass

    def draw(self):
        global_variables.SCREEN_WINDOW.blit(self.image_asset, self.position)
