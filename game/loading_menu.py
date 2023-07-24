import game.global_variables as global_variables
from game.menu import Menu
import pygame_menu
import threading
from game.gameplay_menu import Gameplay_Menu


class Loading_Menu(Menu):
    def __init__(self, is_host):
        self.menu = pygame_menu.Menu(
            "Loading Menu",
            global_variables.SCREEN_WIDTH,
            global_variables.SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )
        self.num_connections =0
        self.menu.add.vertical_margin(30)
        self.menu.add.vertical_margin(30)

        if(is_host):
            active_connections = self.menu.add.label("Number of players joined: {}".format(self.num_connections), font_size=30)
            self.menu.add.button("START GAME", self.navigate_to_gameplay_menu)
            threading.Thread(target=self.new_connections_listener).start()
        else:
            waiting_text = self.menu.add.label("Waiting for host...", font_size=30)
            threading.Thread(target=self.listen_for_host_starting_game).start()

        
    def update_menu(self):
        if self.num_connections_label is not None:
            self.num_connections_label.set_title("Number of players joined: {}".format(self.num_connections))

    def new_connections_listener(self):
        while True:
            if self.num_connections != global_variables.NUMBER_CONNECTIONS:
                self.num_connections = global_variables.NUMBER_CONNECTIONS
                self.update_menu()
                break
        self.navigate_to_gameplay_menu

    def listen_for_host_starting_game(self):
        while True:
            if global_variables.GAME_STARTED:
                self.navigate_to_gameplay_menu()  
                break 

    def waiting_for_game_starting(self):
        pass
        
    def main(self):
        self.menu.mainloop(global_variables.SCREEN_WINDOW)

    def navigate_to_gameplay_menu(self):
        self.gameplay_menu=Gameplay_Menu()
        self.menu._open(self.gameplay_menu.menu)

        pass

    def back_to_main_menu(self):
        self.menu._back()

    def on_ip_address_change(self, value):
        global_variables.HOST_IP_ADDRESS = value
        pass

    def on_port_no_change(self, value):
        global_variables.HOST_PORT = value
        pass
