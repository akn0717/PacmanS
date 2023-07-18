import global_configs
from menus.menu import Menu
import pygame_menu


class Client_Menu(Menu):
    def __init__(self):
        self.menu = pygame_menu.Menu(
            "Client Menu",
            global_configs.SCREEN_WIDTH,
            global_configs.SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )
        
        self.ip_address_input = self.menu.add.text_input(
            "Enter HOST IP ADDRESS: ",
            default="",
            onchange=self.on_ip_address_change,
        )
        self.menu.add.vertical_margin(30)
        self.port_number_input = self.menu.add.text_input(
             "Enter HOST PORT: ",
             default="",
             onchange=self.on_port_no_change
		)
        self.menu.add.vertical_margin(30)
        self.menu.add.button("Continue", self.navigate_to_gameplay_menu)
        self.menu.add.vertical_margin(30)
        self.menu.add.button("Back", self.back_to_main_menu)

    def main(self):
        self.menu.mainloop(global_configs.SCREEN_WINDOW)

    def navigate_to_gameplay_menu(self):
        # gameplay_menu = GameplayMenu()
        # gameplay_menu.main()
        pass

    def back_to_main_menu(self):
         self.menu.reset(1) 
         # TO PREVENT CIRCULAR IMPORT ISSUE
         from menus.main_menu import Main_Menu
         main_menu = Main_Menu()
         main_menu.main()
        
    def on_ip_address_change(self, value):
        global_configs.HOST_IP_ADDRESS=value
        pass
    def on_port_no_change(self, value):
        global_configs.HOST_PORT=value
        pass
