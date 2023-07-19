import pygame

# Initialize Pygame
pygame.init()

# Set up the window dimensions
window_width = 1280
window_height = 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Scoreboard")


font = pygame.font.Font(pygame.font.get_default_font(), 20)

# Define the players and their scores
players = ["Player 1", "Player 2", "Player 3", "Player 4"]
scores = [1, 2, 3, 4]

# Define the colors for each player
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the window with a white background
    window.fill((255, 255, 255))

    # Display the scores in the four corners
    for i in range(4):
        score_text = font.render(f"{players[i]}: {scores[i]}", True, colors[i])
        if i == 0 or i == 2:
            window.blit(score_text, (20, 20))
        else:
            text_width = score_text.get_width()
            window.blit(score_text, (window_width - 20 - text_width, 20))
        
        if i == 1 or i == 2:
            text_height = score_text.get_height()
            window.blit(score_text, (20, window_height - 20 - text_height))
        else:
            text_width = score_text.get_width()
            text_height = score_text.get_height()
            window.blit(score_text, (window_width - 20 - text_width, window_height - 20 - text_height))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
