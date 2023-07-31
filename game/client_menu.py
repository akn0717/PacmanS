import game.global_variables as global_variables
from game.menu import Menu
import pygame_menu
from game.loading_menu import Loading_Menu
from network.Game_Client import Game_Client


class Client_Menu(Menu):
    def __init__(self):
        self.menu = pygame_menu.Menu(
            "Client Menu",
            global_variables.BOARD_WIDTH,
            global_variables.BOARD_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )

        self.inputted_host_ip = ""
        self.inputted_host_port = 0

        self.error_widget = self.menu.add.label("", font_color=(255, 0, 0))
        self.menu.add.vertical_margin(30)
        self.ip_address_input = self.menu.add.text_input(
            "Enter HOST IP ADDRESS: ",
            default="",
            onchange=self.on_ip_address_change,
        )
        self.menu.add.vertical_margin(30)
        self.port_number_input = self.menu.add.text_input(
            "Enter HOST PORT: ", default="", onchange=self.on_port_no_change
        )
        self.menu.add.vertical_margin(30)
        self.menu.add.button("Connect", self.navigate_to_gameplay_menu)
        self.menu.add.vertical_margin(30)
        self.menu.add.button("Back", self.back_to_main_menu)

    def main(self):
        self.menu.mainloop(global_variables.SCREEN_WINDOW)

    def navigate_to_gameplay_menu(self):
        self.error_widget.set_title("Connecting...")
        game_client = Game_Client()
        success = game_client.connect(self.inputted_host_ip, self.inputted_host_port)
        if success != -1:
            print("Connected!")
        else:
            print("Failed to connect!")
            self.error_widget.set_title("Failed to connect to server!")
            return

        self.menu.disable()
        self.loading_menu = Loading_Menu(game_client=game_client)
        self.loading_menu.main()

    def back_to_main_menu(self):
        self.error_widget.set_title("")
        self.menu._back()

    def on_ip_address_change(self, value):
        # for testing. Not sure if global variable one is not needed anymore
        global_variables.HOST_IP_ADDRESS = value
        self.inputted_host_ip = value
        pass

    def on_port_no_change(self, value):
        global_variables.HOST_PORT = value
        self.inputted_host_port = value

        pass
