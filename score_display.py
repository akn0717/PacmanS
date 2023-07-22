import pygame
import random

pygame.init()

window_width = 1280
window_height = 720
window = pygame.display.set_mode((window_width, window_height))

clock = pygame.time.Clock()

font = pygame.font.Font(pygame.font.get_default_font(), 20)
margin = 50

players = ["Player 1", "Player 2", "Player 3", "Player 4"]
scores = [111, 222, 333, 444]

# Define the colors for each player
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]

image_path = "assets/Crown.svg"
image = pygame.image.load(image_path)
image = pygame.transform.scale(image, (30, 50))


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
            text_x = margin
            text_y = margin
            window.blit(score_text, (text_x, text_y))

            # draw the crown after the player with highest score
            if scores[i] == max(scores):
                window.blit(image, (text_width + text_x, text_y - 20))
            i += 1

        elif i == 1:        # player 2
            score_text = font.render(f"{players[i]}: {scores[i]}", True, colors[i])
            text_width = score_text.get_width()
            text_x = window_width - margin - text_width
            text_y = margin
            window.blit(score_text, (text_x, text_y))

            # draw the crown after the player with highest score
            if scores[i] == max(scores):
                window.blit(image, (text_width + text_x, text_y - 20))
            i += 1

        elif i == 2:        # player 3
            score_text = font.render(f"{players[i]}: {scores[i]}", True, colors[i])
            text_width = score_text.get_width()
            text_height = score_text.get_height()
            text_x = margin
            text_y = window_height - margin - text_height
            window.blit(score_text, (text_x, text_y))      

            # draw the crown after the player with highest score
            if scores[i] == max(scores):
                window.blit(image, (text_width + text_x, text_y - 20))   
            i += 1   

        else:               # player 4
            score_text = font.render(f"{players[i]}: {scores[i]}", True, colors[i])
            text_width = score_text.get_width()
            text_height = score_text.get_height()
            text_x = window_width - margin - text_width
            text_y = window_height - margin - text_height
            window.blit(score_text, (text_x, text_y))

            # draw the crown after the player with highest score
            if scores[i] == max(scores):
                window.blit(image, (text_width + text_x, text_y - 20))
            i += 1
        

        
    # for testing
    scores = [random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000)]

    pygame.display.flip()
    clock.tick(0.5)

pygame.quit()
