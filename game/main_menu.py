import game.global_configs as global_configs
from game.base_menu import Menu
import pygame
import pygame_menu


class Main_Menu(Menu):
    def __init__(self):
        super().__init__()
        self.menu = pygame_menu.Menu(
            "Main Menu",
            global_configs.SCREEN_WIDTH,
            global_configs.SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )

        self.start_button = self.menu.add.button("Start", self.start_game)
        self.setting_button = self.menu.add.button("Setting", self.setting)
        self.exit_button = self.menu.add.button("Exit", self.exit_game)

    def main(self):
        self.menu.mainloop(global_configs.SCREEN_WINDOW)

    def start_game(self):
        pass

    def setting(self):
        pass

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
