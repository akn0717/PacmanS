import pygame
import pygame_menu

pygame.init()

window_width = 1280 
window_height = 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("PacmanS")
menu = pygame_menu.Menu("Main menu", 800, 400, theme=pygame_menu.themes.THEME_BLUE)

def start_game():
    print("Starting the game...")

def setting():
    pass

def exit_game():
    pygame.quit()

start_button = menu.add.button("Start", start_game)
setting_button = menu.add.button("Setting", setting)
exit_button = menu.add.button("Exit", exit_game)

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

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                

    # Render the menu
    window.fill((50, 50, 50))  # Fill the window with black color
    menu.draw(window)
    
    clock.tick(FPS)
    pygame.display.flip()
    menu.mainloop(window)

pygame.quit()
print("Test Notification")