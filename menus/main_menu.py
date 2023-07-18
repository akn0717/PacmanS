import global_configs
from menus.menu import Menu
import pygame
import pygame_menu


class Main_Menu(Menu):
    def __init__(self):
        self.menu = pygame_menu.Menu(
            "Main Menu",
            global_configs.SCREEN_WIDTH,
            global_configs.SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE,
        )

        self.join_as_host = self.menu.add.button("Join As Host", self.navigate_to_host_menu)
        self.menu.add.vertical_margin(30)
        self.join_as_client = self.menu.add.button("Join As Client", self.navigate_to_client_menu)
        self.menu.add.vertical_margin(30)
        self.exit_button = self.menu.add.button("Exit", self.exit_game)

    def main(self):
        self.menu.mainloop(global_configs.SCREEN_WINDOW)

    def navigate_to_host_menu(self):
        self.menu.reset(1) 
        from menus.host_menu import Host_Menu
        host_menu = Host_Menu()
        host_menu.main()

    def navigate_to_client_menu(self):
        self.menu.reset(1) 
        from menus.client_menu import Client_Menu
        client_menu = Client_Menu()
        client_menu.main()

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
