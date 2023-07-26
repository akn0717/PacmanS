from multiprocessing import Lock
from game.canvas import Canvas
from game.game_sprites import Pacman
import game.global_variables as global_variables
import game.global_constants as global_constants
from game.menu import Menu
import pygame_menu
import threading
from game.gameplay_menu import Gameplay_Menu
import time


class Loading_Menu(Menu):
    def __init__(self, is_host, game_client=None):
        self.menu = pygame_menu.Menu(
            "Loading Menu",
            global_variables.SCREEN_WIDTH,
            global_variables.SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )
        self.num_connections = 0
        self.menu.add.vertical_margin(30)
        self.menu.add.vertical_margin(30)
        self.game_client = game_client
        global_variables.MUTEX_CANVAS = Lock()
        global_variables.MUTEX_CANVAS_CELLS = [
            [Lock() for _ in range(global_constants.CANVAS_SIZE[1])]
            for _ in range(global_constants.CANVAS_SIZE[0])
        ]
        global_variables.CANVAS = Canvas(None)
        global_variables.PLAYERS = [Pacman(0)] * 4
        if is_host:
            self.active_connections = self.menu.add.label(
                "Number of players joined: {}".format(self.num_connections),
                font_size=30,
            )
            self.menu.add.button("START GAME", self.navigate_to_gameplay_menu)
            threading.Thread(target=self.new_connections_listener).start()
        else:
            waiting_text = self.menu.add.label("Waiting for host...", font_size=30)
            threading.Thread(target=self.listen_for_host_starting_game).start()

    def update_menu(self):
        if self.active_connections is not None:
            self.active_connections.set_title(
                "Number of players: {}".format(self.num_connections)
            )

    def new_connections_listener(self):
        while True:
            if (
                global_variables.NUMBER_CONNECTIONS != None
                and self.num_connections != global_variables.NUMBER_CONNECTIONS
            ):
                self.num_connections = global_variables.NUMBER_CONNECTIONS
                self.update_menu()
                time.sleep(1)
                # maybe need thread to sleep for 1 sec

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
        self.gameplay_menu = Gameplay_Menu()
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
