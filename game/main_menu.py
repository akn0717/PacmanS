import game.global_variables as global_variables
from game.menu import Menu
from game.host_menu import Host_Menu
from game.client_menu import Client_Menu

import pygame
import pygame_menu


class Main_Menu(Menu):
    def __init__(self):
        super().__init__()
        self.menu = pygame_menu.Menu(
            "Main Menu",
            global_variables.SCREEN_WIDTH,
            global_variables.SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )

        self.menu.add.button("Host A Game", self.navigate_to_host_menu)
        self.menu.add.vertical_margin(30)
        self.menu.add.button("Join As Client", self.navigate_to_client_menu)
        self.menu.add.vertical_margin(30)
        self.exit_button = self.menu.add.button("Exit", self.exit_game)
        self.client_menu=Client_Menu()
        self.host_menu=Host_Menu()

    def main(self):
        self.menu.mainloop(global_variables.SCREEN_WINDOW)

    def navigate_to_host_menu(self):
        self.menu._open(self.host_menu.menu)

    def navigate_to_client_menu(self):
        self.menu._open(self.client_menu.menu)

    def exit_game(self):
        pygame.quit()


# def on_hover_enter():
#     button = menu.get_selected_widget()
#     button.set_font_shadow(enabled=True, color=(0, 0, 0), position=None, offset=2)

# def on_hover_exit():
#     button = menu.get_selected_widget()
#     button.set_font_shadow(enabled=False, color=(0, 0, 0), position=None, offset=2)

# pygame_menu.widgets.Widget.set_onmouseover(start_button, on_hover_enter)
# pygame_menu.widgets.Widget.set_onmouseleave(start_button, on_hover_exit)
# pygame_menu.widgets.Widget.set_onmouseover(setting_button, on_hover_enter)
# pygame_menu.widgets.Widget.set_onmouseleave(setting_button, on_hover_exit)
# pygame_menu.widgets.Widget.set_onmouseover(exit_button, on_hover_enter)
# pygame_menu.widgets.Widget.set_onmouseleave(exit_button, on_hover_exit)
