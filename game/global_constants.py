import pygame

CANVAS_SIZE = (10, 10)
PRIMARY_COLOR = (255, 255, 255)
IMAGE_ASSET_EMPTY_BLOCK = pygame.image.load("../assets/EmptyBlock.png")
IMAGE_ASSET_WALL_BLOCK = pygame.image.load("../assets/Block.png")
IMAGE_ASSET_DOT = pygame.image.load("")

num_players = 4
# TODO get player ids from the server and assign them with each image color
IMAGE_ASSET_PLAYERS = [
    pygame.image.load("../assets/PacmanYellow.png")
    .convert_alpha()
    .set_colorkey(((255, 255, 255) / num_players) * i)
    for i in range(num_players)
]

MOVE_DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
