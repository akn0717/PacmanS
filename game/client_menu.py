from game.client_loading_menu import Client_Loading_Menu
import game.global_variables as global_variables
from game.menu import Menu
import pygame_menu
from game.host_loading_menu import Host_Loading_Menu
from network.Game_Client import Game_Client


class Client_Menu(Menu):
    def __init__(self):
        # init the menu using pygame_menu lib
        self.menu = pygame_menu.Menu(
            "Client Menu",
            global_variables.SCREEN_WIDTH,
            global_variables.SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )

        # variabl to take inputs from user
        self.inputted_host_ip = ""
        self.inputted_host_port = 0

        # Error label activated if connection to server fails
        self.error_widget = self.menu.add.label("", font_color=(255, 0, 0))
        self.menu.add.vertical_margin(30)
        # show input field and text to the screen to enter IP and Port
        self.ip_address_input = self.menu.add.text_input(
            "Enter HOST IP ADDRESS: ",
            default="",
            onchange=self.on_ip_address_change,
        )
        self.menu.add.vertical_margin(30)
        self.port_number_input = self.menu.add.text_input(
            "Enter HOST PORT: ", default="", onchange=self.on_port_no_change
        )
        # Buttons to attempt to start connection or go back
        self.menu.add.vertical_margin(30)
        self.menu.add.button("Connect", self.connect_to_server)
        self.menu.add.vertical_margin(30)
        self.menu.add.button("Back", self.back_to_main_menu)

    def main(self):
        # call mainloop function of pygame_menu
        self.menu.mainloop(global_variables.SCREEN_WINDOW)

    def connect_to_server(self):
        self.error_widget.set_title("Connecting...")
        # initialize game_client and attempt connection to inputted IP and Port
        self.game_client = Game_Client()
        success = self.game_client.connect(
            self.inputted_host_ip, self.inputted_host_port
        )
        if success != -1:
            print("Connected!")
            self.error_widget.set_title("Connected!")

            # If connected, disable menu, and navigate to loading menu
            self.menu.disable()
            self.client_load_menu = Client_Loading_Menu(self.game_client)
            self.client_load_menu.main()
        else:
            print("Failed to connect!")
            self.error_widget.set_title("Failed to connect to server!")
            return

    def back_to_main_menu(self):
        self.error_widget.set_title("")
        self.menu._back()

    def on_ip_address_change(self, value):
        self.inputted_host_ip = value

    def on_port_no_change(self, value):
        self.inputted_host_port = value
