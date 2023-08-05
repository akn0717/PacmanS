from game.gameplay_menu import Gameplay_Menu
import game.global_variables as global_variables
import pygame_menu
import pygame
from game.menu import Menu
from network.Game_Client import Game_Client
import game.global_constants as global_constants
from pygame.locals import USEREVENT


class Client_Loading_Menu(Menu):
    def __init__(self, game_client) -> None:
        self.game_client = game_client
        super().__init__()

    def main(self):
        # init the menu using pygame_menu lib
        self.menu = pygame_menu.Menu(
            "Loading Menu",
            global_variables.SCREEN_WIDTH,
            global_variables.SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )

        clock = pygame.time.Clock()
        FPS = 15

        # show text to the screen
        self.menu.add.label("Connected!", font_size=30)
        self.menu.add.vertical_margin(30)
        self.menu.add.label("Waiting for host...", font_size=30)

        # assert if the variable is not the correct type
        assert isinstance(global_variables.SCREEN_WINDOW, pygame.Surface)

        # fill the background to the primary color
        global_variables.SCREEN_WINDOW.fill(global_constants.PRIMARY_COLOR)

        isRunning = True
        while isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                    self.game_client.close_socket()
                    return

            if global_variables.GAME_STARTED == True:
                # if host start the game, close this menu and navigate to gameplay menu.
                self.menu.disable()
                self.gameplay_menu = Gameplay_Menu(self.game_client)
                self.gameplay_menu.main()
                return
            # Update display
            pygame.display.update()
            # player will move every tick
            clock.tick(FPS)
