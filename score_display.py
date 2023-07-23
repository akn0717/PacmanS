import pygame
import random

pygame.init()

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

clock = pygame.time.Clock()

font = pygame.font.Font(pygame.font.get_default_font(), 30)
margin = 50
space = 20

players = ["Player 1", "Player 2", "Player 3", "Player 4"]
scores = [111, 222, 333, 444]

# Define the colors for each player
colors = [(255, 0, 0), (0, 128, 0), (0, 0, 255), (255, 200, 0)] # red, green, blue, yellow

crown_path = "assets/Crown.svg"
icon_crown = pygame.image.load(crown_path)
icon_crown = pygame.transform.scale(icon_crown, (30, 50))

icon_pacman_size = 50

pacman_red_path = "assets/PacmanRed.svg"
icon_pacman_red = pygame.image.load(pacman_red_path)
icon_pacman_red = pygame.transform.scale(icon_pacman_red, (icon_pacman_size, icon_pacman_size))

pacman_green_path = "assets/PacmanGreen.svg"
icon_pacman_green = pygame.image.load(pacman_green_path)
icon_pacman_green = pygame.transform.scale(icon_pacman_green, (icon_pacman_size, icon_pacman_size))

pacman_blue_path = "assets/PacmanBlue.svg"
icon_pacman_blue = pygame.image.load(pacman_blue_path)
icon_pacman_blue = pygame.transform.scale(icon_pacman_blue, (icon_pacman_size, icon_pacman_size))

pacman_yellow_path = "assets/PacmanYellow.svg"
icon_pacman_yellow = pygame.image.load(pacman_yellow_path)
icon_pacman_yellow = pygame.transform.scale(icon_pacman_yellow, (icon_pacman_size, icon_pacman_size))



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background color
    window.fill((255, 255, 255))


    for i in range(4):
        
        if i == 0:          # player 1
            score_text = font.render(f"{players[i]}: {scores[i]}", True, colors[i])
            text_width = score_text.get_width()
            text_height = score_text.get_height()
            text_x = margin
            text_y = margin
            window.blit(score_text, (text_x, text_y))
            icon_x = text_x + text_width + space
            icon_y = text_y - text_height / 2
            window.blit(icon_pacman_red, (icon_x, icon_y))

            # draw the crown after the player with highest score
            if scores[i] == max(scores):
                window.blit(icon_crown, (text_width + text_x + icon_pacman_size, text_y - 20))
            i += 1

        elif i == 1:        # player 2
            score_text = font.render(f"{players[i]}: {scores[i]}", True, colors[i])
            text_width = score_text.get_width()
            text_height = score_text.get_height()
            icon_x = window_width - margin - text_width - space - icon_pacman_size
            icon_y = margin
            window.blit(icon_pacman_green, (icon_x, icon_y))
            text_x = icon_x + icon_pacman_size + space
            text_y = icon_y + icon_pacman_size / 2 - text_height / 2
            window.blit(score_text, (text_x, text_y))

            # draw the crown after the player with highest score
            if scores[i] == max(scores):
                window.blit(icon_crown, (text_width + text_x, text_y - 20))
            i += 1

        elif i == 2:        # player 3            
            score_text = font.render(f"{players[i]}: {scores[i]}", True, colors[i])
            text_width = score_text.get_width()
            text_height = score_text.get_height()
            text_x = margin
            text_y = window_height - margin - text_height
            window.blit(score_text, (text_x, text_y))
            icon_x = text_x + text_width + space
            icon_y = text_y - text_height / 2
            window.blit(icon_pacman_blue, (icon_x, icon_y))

            # draw the crown after the player with highest score
            if scores[i] == max(scores):
                window.blit(icon_crown, (text_width + text_x, text_y - 20))   
            i += 1   

        else:               # player 4
            score_text = font.render(f"{players[i]}: {scores[i]}", True, colors[i])
            text_width = score_text.get_width()
            text_height = score_text.get_height()
            icon_x = window_width - margin - text_width - space - icon_pacman_size
            icon_y = window_height - margin - text_height
            window.blit(icon_pacman_yellow, (icon_x, icon_y))
            text_x = icon_x + icon_pacman_size + space
            text_y = icon_y + icon_pacman_size / 2 - text_height / 2
            window.blit(score_text, (text_x, text_y))

            # draw the crown after the player with highest score
            if scores[i] == max(scores):
                window.blit(icon_crown, (text_width + text_x, text_y - 20))
            i += 1
        

        
    # for testing
    scores = [random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000)]

    pygame.display.flip()
    clock.tick(0.5)

pygame.quit()
