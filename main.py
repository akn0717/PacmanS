import argparse
import pygame
import game.global_variables as global_variables
from game.gameplay_menu import *


def init():
    pygame.init()
    global_variables.SCREEN_WINDOW = pygame.display.set_mode((1280, 800))
    # (
    #     global_variables.SCREEN_WIDTH,
    #     global_variables.SCREEN_HEIGHT,
    # ) = global_variables.SCREEN_WINDOW.get_size()
    (
        global_variables.SCREEN_WIDTH,
        global_variables.SCREEN_HEIGHT,
    ) = (
        global_variables.SCREEN_WINDOW.get_height(),
        global_variables.SCREEN_WINDOW.get_height()
    )

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


    global_variables.SCORE_DISPLAY_FONT =  pygame.font.Font(pygame.font.get_default_font(), 30)
    global_variables.ICON_CROWN = pygame.transform.scale(
        pygame.image.load("assets/PacmanRed.svg"), (50, 50)
    )
    pygame.display.set_caption("PacmanS")


def run(args):
    print("Starting the game...")
    # TODO get player ids from the server and assign them with each image color

    menu = Gameplay_Menu()
    menu.main()
    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    init()
    run(args)
