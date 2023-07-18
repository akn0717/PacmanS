import argparse
import pygame
import global_configs
from menus.main_menu import Main_Menu


def run(args):
    print("Starting the game...")
    pygame.init()
    global_configs.SCREEN_WINDOW = pygame.display.set_mode()
    (
        global_configs.SCREEN_WIDTH,
        global_configs.SCREEN_HEIGHT,
    ) = global_configs.SCREEN_WINDOW.get_size()
    pygame.display.set_caption("PacmanS")
    menu = Main_Menu()
    while True:
        menu = menu.main()
        if not (menu):
            break
    pygame.none(
    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    run(args)
