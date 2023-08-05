import game.global_variables as global_variables
from game.menu import Menu
from game.host_menu import Host_Menu
from game.client_menu import Client_Menu
import game.global_constants as global_constants
import pygame
import pygame_menu


class Main_Menu(Menu):
    def __init__(self):
        super().__init__()
        # init the menu using pygame_menu lib
        self.menu = pygame_menu.Menu(
            "Main Menu",
            global_variables.SCREEN_WIDTH,
            global_variables.SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )

        # buttons to enter the game as a host/client
        self.menu.add.button("Host A Game", self.navigate_to_host_menu)
        self.menu.add.vertical_margin(30)
        self.menu.add.button("Join As Client", self.navigate_to_client_menu)
        self.menu.add.vertical_margin(30)
        self.exit_button = self.menu.add.button("Exit", self.exit_game)

        # init the client and host menus
        self.client_menu = Client_Menu()
        self.host_menu = Host_Menu()

    def main(self):
        self.menu.mainloop(global_variables.SCREEN_WINDOW)

    # navigate according to user selection
    def navigate_to_host_menu(self):
        self.menu._open(self.host_menu.menu)

    def navigate_to_client_menu(self):
        self.menu._open(self.client_menu.menu)

    def exit_game(self):
        self.menu.disable()
