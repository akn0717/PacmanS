import pygame
import game.global_constants as global_constants
import game.global_variables as global_variables
import sys


class Score_Menu:
    def __init__(self):
        # init the menu
        self.surface = pygame.display.set_mode(
            (global_variables.SCREEN_WIDTH, global_variables.SCREEN_HEIGHT)
        )
        self.surface.fill(global_constants.PRIMARY_COLOR)
        self.players = global_variables.PLAYERS

    def display_individual_player_stats(
        self, player_name, score, player_image, y_offset
    ):
        font = pygame.font.Font(None, 32)

        icon_size = (40, 40)  # Set the desired icon size for player_image
        player_image = pygame.transform.scale(player_image, icon_size)

        player_info_surface = pygame.Surface((self.surface.get_width(), 50))
        player_info_surface.fill(global_constants.PRIMARY_COLOR)

        player_info_surface.blit(player_image, (10, 5))
        # set up all player details and render name, score
        player_name_text = font.render(player_name, True, (255, 255, 255))
        score_text = font.render(str(score), True, (255, 255, 255))
        player_info_surface.blit(player_name_text, (80, 5))
        player_info_surface.blit(score_text, (self.surface.get_width() - 80, 5))

        self.surface.blit(player_info_surface, (0, y_offset))

    def display_disconnected_from_host(self):
        # if host disconnect during game, show players disconnected text
        self.surface.fill(global_constants.PRIMARY_COLOR)
        font = pygame.font.Font(None, 72)
        disconnected_text = font.render("DISCONNECTED FROM HOST", True, (255, 0, 0))
        self.surface.blit(
            disconnected_text,
            (
                (self.surface.get_width() - disconnected_text.get_width()) // 2,
                (self.surface.get_height() - disconnected_text.get_height()) // 2,
            ),
        )

        pygame.display.flip()

    def display_scores(self):
        player_list = []
        score_list = []
        for i in self.players:
            score_list.append(self.players[i].score)
            player_list.append(i)

        # sort the players according to the highest score
        player_score_dict = dict(zip(player_list, score_list))
        sorted_player_score_dict = dict(
            sorted(player_score_dict.items(), key=lambda item: item[1], reverse=True)
        )

        font = pygame.font.Font(None, 64)
        # display the scores heading
        title_text = font.render("SCORES", True, (255, 255, 255))
        self.surface.blit(
            title_text, ((self.surface.get_width() - title_text.get_width()) // 2, 20)
        )
        y_offset = 100
        # assign player image according to player id
        for player, score in sorted_player_score_dict.items():
            player_name = f"Player {player + 1}"

            # display each player scores according to the order of score
            self.display_individual_player_stats(
                player_name, score, self.players[player].image_assets[0], y_offset
            )
            y_offset += 70

        # get winning player stat by taking the max of the sorted dictionary
        winning_player = max(sorted_player_score_dict, key=sorted_player_score_dict.get)
        winning_player_name = f"Player {winning_player + 1}"

        # Display the winning player text
        font = pygame.font.Font(None, 48)
        winning_text = font.render(
            f"{winning_player_name} WINS!", True, (255, 255, 255)
        )
        self.surface.blit(
            winning_text,
            ((self.surface.get_width() - winning_text.get_width()) // 2, y_offset + 20),
        )
        pygame.display.flip()

    def main(self):
        pygame.init()
        pygame.display.set_caption("Player Scores")

        # show score menu only if game completed, if disconnected, show disconnected from host
        if global_variables.DISCONNECTED_FROM_HOST:
            self.display_disconnected_from_host()
        else:
            self.display_scores()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with global_variables.QUIT_GAME_LOCK:
                        global_variables.QUIT_GAME = True
                    return
        sys.exit()
