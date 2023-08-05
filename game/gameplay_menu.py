from game.menu import Menu
import pygame
import game.global_constants as global_constants
import game.global_variables as global_variables
from game.global_constants import Direction
from game.score_menu import Score_Menu


class Gameplay_Menu(Menu):
    def __init__(self, game_client) -> None:
        super().__init__()
        self.game_client = game_client
        self.score_list = []

    def main(self):
        isRunning = True
        clock = pygame.time.Clock()
        FPS = 30
        updateIteration = 0
        while isRunning:
            # if GAME_OVER is true, this means that the server has sent a message to end the game
            # for all players. The players are then navigated to the score_menu
            with global_variables.GAME_OVER_LOCK:
                if global_variables.GAME_OVER:
                    score_menu = Score_Menu()
                    score_menu.main()
                    return
            with global_variables.DISCONNECTED_FROM_HOST_LOCK:
                if global_variables.DISCONNECTED_FROM_HOST:
                    score_menu = Score_Menu()
                    score_menu.main()
                    return
            for event in pygame.event.get():
                # if player quit the game, close the client's socket
                if event.type == pygame.QUIT:
                    isRunning = False
                    with global_variables.QUIT_GAME_LOCK:
                        global_variables.QUIT_GAME = True
                        self.game_client.close_socket()
                    return
                # change player moving direction according to player input
                elif event.type == pygame.KEYDOWN:
                    if (
                        event.key == pygame.K_UP
                    ):  # key arrow up pressing, set the current direction to up
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].setDirection(Direction.UP.value)
                    elif event.key == pygame.K_DOWN:  # key arrow down pressing
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].setDirection(Direction.DOWN.value)
                    elif event.key == pygame.K_LEFT:  # key arrow left pressing
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].setDirection(Direction.LEFT.value)
                    elif event.key == pygame.K_RIGHT:  # key arrow right pressing
                        global_variables.PLAYERS[
                            global_variables.PLAYER_ID
                        ].setDirection(Direction.RIGHT.value)

            # Clear display
            assert isinstance(global_variables.SCREEN_WINDOW, pygame.Surface)
            global_variables.SCREEN_WINDOW.fill(global_constants.PRIMARY_COLOR)

            # Update
            global_variables.CANVAS.update()
            # player will move every tick

            # movement are sent by interval, this is to reduce number of movement requesting messages avoiding server overloading.
            if updateIteration % 30 == 0:
                global_variables.MOVING_REQUEST = False

            if updateIteration % 10 == 0:
                with global_variables.MUTEX_MOVING_REQUEST:
                    if global_variables.MOVING_REQUEST == False:
                        with global_variables.MUTEX_PLAYERS[global_variables.PLAYER_ID]:
                            global_variables.PLAYERS[global_variables.PLAYER_ID].move(
                                self.game_client
                            )

            updateIteration += 1

            # display the current board state
            global_variables.CANVAS.draw()

            # display player on the canvas
            for player_id in global_variables.PLAYERS:
                global_variables.PLAYERS[player_id].draw()

            global_variables.CANVAS.score_display(global_variables.PLAYERS)

            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()
