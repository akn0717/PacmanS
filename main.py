import argparse
import pygame
import game.global_variables as global_variables
from game.gameplay_menu import *


def init():
    pygame.init()
    global_variables.SCREEN_WINDOW = pygame.display.set_mode((1280, 720))
    (
        global_variables.SCREEN_WIDTH,
        global_variables.SCREEN_HEIGHT,
    ) = global_variables.SCREEN_WINDOW.get_size()
    (
        global_variables.BOARD_WIDTH,
        global_variables.BOARD_HEIGHT,
    ) = (
        global_variables.SCREEN_HEIGHT,
        global_variables.SCREEN_HEIGHT,
    )

    global_variables.CANVAS_UNIT = (
        int(global_variables.BOARD_HEIGHT / global_constants.CANVAS_SIZE[0]),
        int(global_variables.BOARD_WIDTH / global_constants.CANVAS_SIZE[1]),
    )

    global_variables.BOARD_MARGIN = (
        (global_variables.SCREEN_WIDTH - 
        global_variables.CANVAS_UNIT[1] * global_constants.CANVAS_SIZE[0]) / 2
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


    global_variables.SCORE_FONT = pygame.font.Font(
        pygame.font.get_default_font(), 
        global_variables.CANVAS_UNIT[0]
    )
    global_variables.ICON_CROWN =  pygame.transform.scale(
        pygame.image.load("assets/Crown.svg"), 
        (global_variables.CANVAS_UNIT[0] * 3, global_variables.CANVAS_UNIT[1] * 4)
    )

    global_variables.ICON_PACMAN_SIZE = global_variables.CANVAS_UNIT[0] * 2

    global_variables.ICON_PACMAN_RED = pygame.transform.scale(
        pygame.image.load("assets/PacmanRed.svg"),
    (global_variables.ICON_PACMAN_SIZE, global_variables.ICON_PACMAN_SIZE)
    )

    global_variables.ICON_PACMAN_GREEN = pygame.transform.scale(
        pygame.image.load("assets/PacmanGreen.svg"), 
        (global_variables.ICON_PACMAN_SIZE, global_variables.ICON_PACMAN_SIZE)
    )

    global_variables.ICON_PACMAN_BLUE = pygame.transform.scale(
        pygame.image.load("assets/PacmanBlue.svg"), 
        (global_variables.ICON_PACMAN_SIZE, global_variables.ICON_PACMAN_SIZE)
    )

    global_variables.ICON_PACMAN_YELLOW = pygame.transform.scale(
        pygame.image.load("assets/PacmanYellow.svg"),
        (global_variables.ICON_PACMAN_SIZE, global_variables.ICON_PACMAN_SIZE)
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
