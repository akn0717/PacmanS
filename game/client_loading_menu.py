from game.gameplay_menu import Gameplay_Menu
import game.global_variables as global_variables
import pygame_menu
import pygame
from game.menu import Menu
from network.Game_Client import Game_Client
import game.global_constants as global_constants
from pygame.locals import USEREVENT 
class Client_Loading_Menu(Menu):
    def __init__(self,game_client) -> None:
        self.game_client= game_client
        super().__init__()


    def main(self):
        self.menu = pygame_menu.Menu(
            "Loading Menu",
            global_variables.BOARD_WIDTH,
            global_variables.BOARD_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )
        isRunning = True
        clock = pygame.time.Clock()
        FPS = 15

        waiting_text = self.menu.add.label("Waiting for host...", font_size=30)

        assert isinstance(global_variables.SCREEN_WINDOW, pygame.Surface)
        global_variables.SCREEN_WINDOW.fill(global_constants.PRIMARY_COLOR)
        while isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                    self.game_client.close_socket()
                    return
                elif global_variables.GAME_STARTED==True:
                    # print("HERE???")
                    self.menu.disable()
                    self.gameplay_menu = Gameplay_Menu(self.game_client)
                    self.gameplay_menu.main()
                    return
            # Clear display
            assert isinstance(global_variables.SCREEN_WINDOW, pygame.Surface)
            global_variables.SCREEN_WINDOW.fill(global_constants.PRIMARY_COLOR)

            # Update
            # player will move every tick

            # Draw the menu
            self.menu.draw(global_variables.SCREEN_WINDOW)
            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()