from game.base_menu import Menu
from game.canvas import Canvas


class gameplay_menu(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.canvas = Canvas(CANVAS_SIZE)

    def main(self):
        pass
