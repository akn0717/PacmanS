import argparse
import pygame
import game.global_variables as global_variables
from game.main_menu import Main_Menu


def run(args):
    print("Starting the game...")
    pygame.init()
    global_variables.SCREEN_WINDOW = pygame.display.set_mode()
    (
        global_variables.SCREEN_WIDTH,
        global_variables.SCREEN_HEIGHT,
    ) = global_variables.SCREEN_WINDOW.get_size()
    pygame.display.set_caption("PacmanS")
    menu = Main_Menu()
    menu.main()
    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    run(args)
