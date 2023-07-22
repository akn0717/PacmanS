import game.global_variables as global_variables
from game.menu import Menu
import pygame_menu


class Client_Menu(Menu):
    def __init__(self):
        self.menu = pygame_menu.Menu(
            "Client Menu",
            global_variables.SCREEN_WIDTH,
            global_variables.SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )

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
        self.menu.add.button("Continue", self.navigate_to_gameplay_menu)
        self.menu.add.vertical_margin(30)
        self.menu.add.button("Back", self.back_to_main_menu)

    def main(self):
        self.menu.mainloop(global_variables.SCREEN_WINDOW)

    def navigate_to_gameplay_menu(self):
        pass

    def back_to_main_menu(self):
        self.menu._back()

    def on_ip_address_change(self, value):
        global_variables.HOST_IP_ADDRESS = value
        pass

    def on_port_no_change(self, value):
        global_configs.HOST_PORT = value
        pass
