import pygame
import game.global_constants as global_constants
import game.global_variables as global_variables
import sys


class Score_Menu:
    def __init__(self):
        self.surface = pygame.display.set_mode((800, 600))  # Create a Pygame surface
        self.surface.fill(global_constants.PRIMARY_COLOR)
        self.players = global_variables.PLAYERS

    def display_player_info(self, player_name, score, player_image, y_offset):
        font = pygame.font.Font(None, 32)

        player_image = pygame.image.load(image_path)
        icon_size = (40, 40)  # Set the desired icon size
        player_image = pygame.transform.scale(player_image, icon_size)

        player_info_surface = pygame.Surface((self.surface.get_width(), 50))
        # player_info_surface.fill(global_constants.PRIMARY_COLOR)

        player_info_surface.blit(player_image, (10, 5))

        player_name_text = font.render(player_name, True, (255, 255, 255))
        score_text = font.render(str(score), True, (255, 255, 255))
        player_info_surface.blit(player_name_text, (80, 5))
        player_info_surface.blit(score_text, (self.surface.get_width() - 80, 5))

        self.surface.blit(player_info_surface, (0, y_offset))

    def display_scores(self):
        self.surface.fill((0, 0, 0))
        player_list = []
        score_list = []
        for i in range(len(self.players)):
            score_list.append(self.players[i].score)
            player_list.append(i)

        player_score_dict = dict(zip(player_list, score_list))
        sorted_player_score_dict = dict(
            sorted(player_score_dict.items(), key=lambda item: item[1], reverse=True)
        )

        font = pygame.font.Font(None, 64)
        title_text = font.render("SCORES", True, (255, 255, 255))
        self.surface.blit(
            title_text, ((self.surface.get_width() - title_text.get_width()) // 2, 20)
        )
        y_offset = 100

        for player, score in sorted_player_score_dict.items():
            player_name = f"Player {player + 1}"
            if player == 0:
                image_path = f"assets/PacmanYellow.svg"
            elif player == 1:
                image_path = f"assets/PacmanRed.svg"
            elif player == 2:
                image_path = f"assets/PacmanGreen.svg"
            elif player == 3:
                image_path = f"assets/PacmanBlue.svg"

            self.display_player_info(
                player_name, score, self.players[player].image_assets[0], y_offset
            )
            y_offset += 70
        pygame.display.flip()

    def main(self):
        pygame.init()
        pygame.display.set_caption("Player Scores")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return

            self.display_scores()
        sys.exit()
