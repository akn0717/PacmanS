from game.base_menu import Menu
from game.canvas import Canvas


class gameplay_menu(Menu):
    def __init__(self, host: str = None) -> None:
        super().__init__()
        if host is not None:  # is a client
            pass
        else:  # is a server, responsible for generating the game board
            self.canvas = Canvas()

    def main(self):
        pass
