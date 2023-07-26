import game.global_variables as global_variables
from game.menu import Menu
import pygame_menu
from game.loading_menu import Loading_Menu
from network.Game_Client import Game_Client
from network.Game_Server import Game_Server


class Host_Menu(Menu):
    def __init__(self):
        self.menu = pygame_menu.Menu(
            "Host Menu",
            global_variables.SCREEN_WIDTH,
            global_variables.SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )

        self.inputted_host_port = 5555

        self.port_number_input = self.menu.add.text_input(
            "Enter HOST PORT: ", default="", onchange=self.on_port_no_change
        )
        self.menu.add.vertical_margin(30)
        self.menu.add.button("Continue", self.navigate_to_loading_menu)
        self.menu.add.vertical_margin(30)
        self.menu.add.button("Back", self.back_to_main_menu)

    def main(self):
        self.menu.mainloop(global_variables.SCREEN_WINDOW)

    def navigate_to_loading_menu(self):
        game_server = Game_Server(int(self.inputted_host_port))
        game_server.initializeGameData()
        game_server.startConnectionListener()

        # Host is also a client and connect to itself
        game_client = Game_Client()
        game_client.connect("127.0.0.1", self.inputted_host_port)

        self.loading_menu = Loading_Menu(
            game_client=game_client, game_server=game_server
        )
        self.menu._open(self.loading_menu.menu)
        pass

    def back_to_main_menu(self):
        self.menu._back()

    def on_port_no_change(self, value):
        self.inputted_host_port = value
        pass
