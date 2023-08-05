import game.global_variables as global_variables
from game.menu import Menu
import pygame_menu
from game.host_loading_menu import Host_Loading_Menu
from network.Game_Client import Game_Client
from network.Game_Server import Game_Server


class Host_Menu(Menu):
    def __init__(self):
        # init the menu using pygame_menu lib
        self.menu = pygame_menu.Menu(
            "Host Menu",
            global_variables.SCREEN_WIDTH,
            global_variables.SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )

        self.game_server = None
        # variable to take inputs from user
        self.inputted_host_port = 0

        # show input field and text to the screen to enter PORT
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

        # try to parse the port if it is valid
        try:
            port = int(self.inputted_host_port)
        except:
            # if it not then don't start the game server
            return

        # initialize the game server with the inputted port
        self.game_server = Game_Server(port)
        self.game_server.initializeGameData()
        # start thread in game server for listening to connections
        self.game_server.startConnectionListener()

        # Host is also a client and connect to itself
        self.game_client = Game_Client()
        self.game_client.connect("127.0.0.1", self.inputted_host_port)
        # Navigate to loading_menu after port input
        self.loading_menu = Host_Loading_Menu(
            game_client=self.game_client, game_server=self.game_server
        )
        self.menu._open(self.loading_menu.menu)

    def back_to_main_menu(self):  # go to back to previous menu
        self.menu._back()

    def on_port_no_change(self, value):
        self.inputted_host_port = value
