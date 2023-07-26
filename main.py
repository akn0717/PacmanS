import argparse
import pygame
import game.global_variables as global_variables
import game.global_constants as global_constants
from game.gameplay_menu import *
from game.main_menu import Main_Menu


def init():
    pygame.init()
    global_variables.SCREEN_WINDOW = pygame.display.set_mode((800, 800))
    (
        global_variables.SCREEN_WIDTH,
        global_variables.SCREEN_HEIGHT,
    ) = global_variables.SCREEN_WINDOW.get_size()

    global_variables.CANVAS_UNIT = (
        int(global_variables.SCREEN_HEIGHT / global_constants.CANVAS_SIZE[0]),
        int(global_variables.SCREEN_WIDTH / global_constants.CANVAS_SIZE[1]),
    )
    global_variables.IMAGE_ASSET_EMPTY_BLOCK = pygame.transform.scale(
        pygame.image.load("assets/EmptyBlock.png"), global_variables.CANVAS_UNIT
    )
    global_variables.IMAGE_ASSET_WALL_BLOCK = pygame.transform.scale(
        pygame.image.load("assets/Block.png"), global_variables.CANVAS_UNIT
    )
    global_variables.IMAGE_ASSET_DOT = pygame.transform.scale(
        pygame.image.load("assets/SmallDot.png"), global_variables.CANVAS_UNIT
    )
    global_variables.IMAGE_ASSET_PLAYERS = [
        pygame.transform.scale(
            pygame.image.load("assets/PacmanYellowSingle.png").convert_alpha(),
            global_variables.CANVAS_UNIT,
        )
        for i in range(global_constants.NUM_PLAYERS)
    ]  # TODO: change color of player depending on the player ID
    global_variables.CANVAS = Canvas()
    global_variables.MUTEX_CANVAS = Lock()
    global_variables.MUTEX_CANVAS_CELLS = [
        [Lock() for _ in range(global_constants.CANVAS_SIZE[1])]
        for _ in range(global_constants.CANVAS_SIZE[0])
    ]
    global_variables.MUTEX_PLAYER_ID = Lock()
    global_variables.MUTEX_PLAYERS = [
        Lock() for _ in range(global_constants.NUM_PLAYERS)
    ]
    global_variables.MUTEX_PLAYERS_LIST = Lock()

    global_variables.NUMBER_CONNECTIONS = 0
    global_variables.GAME_STARTED = False
    global_variables.PLAYERS = [Pacman(0)] * 4
    pygame.display.set_caption("PacmanS")


def run(args):
    print("Starting the game...")
    # TODO get player ids from the server and assign them with each image color

    # menu = Loading_Menu(True)
    menu = Main_Menu()
    menu.main()
    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    init()
    run(args)
