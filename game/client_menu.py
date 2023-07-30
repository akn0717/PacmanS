import game.global_variables as global_variables
from game.menu import Menu
import pygame_menu
from game.loading_menu import Loading_Menu
from network.Game_Client import Game_Client
from game.gameplay_menu import Gameplay_Menu



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
        self.menu.add.button("Connect", self.connect_to_server)
        self.menu.add.vertical_margin(30)
        self.menu.add.button("Back", self.back_to_main_menu)

    def main(self):
        self.menu.mainloop(global_variables.SCREEN_WINDOW)

    def connect_to_server(self):
        self.error_widget.set_title("Connecting...")
        self.game_client = Game_Client()
        success = self.game_client.connect(self.inputted_host_ip, self.inputted_host_port)
        if success != -1:
            print("Connected!")
            self.listen_for_game_start(self.game_client)
        else:
            print("Failed to connect!")
            self.error_widget.set_title("Failed to connect to server!")
            return


    def back_to_main_menu(self):
        self.error_widget.set_title("")
        self.menu._back()
    
    def listen_for_game_start(self):
        self.gameplay_menu = Gameplay_Menu(self.game_client)
        self.gameplay_menu.main()

        

    def on_ip_address_change(self, value):
        # for testing. Not sure if global variable one is not needed anymore
        global_variables.HOST_IP_ADDRESS = value
        self.inputted_host_ip = value
        pass

    def on_port_no_change(self, value):
        global_variables.HOST_PORT = value
        self.inputted_host_port = value

        pass
