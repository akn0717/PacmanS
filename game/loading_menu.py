from multiprocessing import Lock
from game.canvas import Canvas
from game.game_sprites import Pacman
import game.global_variables as global_variables
import game.global_constants as global_constants
from game.menu import Menu
import pygame_menu
import pygame
from game.gameplay_menu import Gameplay_Menu
import time


class Loading_Menu(Menu):
    def __init__(self, game_client, game_server=None):
        self.menu = pygame_menu.Menu(
            "Loading Menu",
            global_variables.SCREEN_WIDTH,
            global_variables.SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )
        self.game_server = game_server
        self.num_connections = 0
        self.menu.add.vertical_margin(30)
        self.menu.add.vertical_margin(30)
        self.game_client = game_client

        if self.game_server is not None:
            self.active_connections = self.menu.add.label(
                "Number of players joined: {}".format(
                    global_variables.NUMBER_CONNECTIONS
                ),
                font_size=30,
            )
            self.menu.add.button("START GAME", self.start_game)

        else:
            waiting_text = self.menu.add.label("Waiting for host...", font_size=30)

    def update_menu(self):
        if self.active_connections is not None:
            self.active_connections.set_title(
                "Number of players: {}".format(self.num_connections)
            )

    def new_connections_listener(self):
        while True:
            # print("looping?")
            if global_variables.GAME_STARTED == True:
                # self.menu.disable()
                break
            if (
                global_variables.NUMBER_CONNECTIONS != None
                and self.num_connections != global_variables.NUMBER_CONNECTIONS
            ):
                self.num_connections = global_variables.NUMBER_CONNECTIONS
                self.update_menu()
                time.sleep(1)
                # maybe need thread to sleep for 1 sec

    def start_game(self):
        self.game_server.startGame()
        self.game_server.remove_spawn_dots()
        clock = pygame.time.Clock()
        FPS = 15
        while True:
            with global_variables.GAME_STARTED_LOCK:
                if global_variables.GAME_STARTED:
                    self.navigate_to_gameplay_menu()
                    break
            pygame.display.update()
            clock.tick(FPS)

    def navigate_to_gameplay_menu(self):
        self.menu.disable()
        self.gameplay_menu = Gameplay_Menu(self.game_client)
        self.gameplay_menu.main()

    def back_to_main_menu(self):
        self.menu._back()

    def on_ip_address_change(self, value):
        global_variables.HOST_IP_ADDRESS = value
        pass

    def on_port_no_change(self, value):
        global_variables.HOST_PORT = value
        pass
