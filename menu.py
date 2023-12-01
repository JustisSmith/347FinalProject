import pygame
import sys
from settings import screen_width, screen_height  # Import screen dimensions from settings 

pygame.init()

# Create a window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu")

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
menu_title_font = pygame.font.Font(None, 72)  # Defined a larger font for the title
font = pygame.font.Font(None, 36)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def main_menu():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    return "PLAY"  # Indicate that the game should start
                if event.key == pygame.K_o:
                    return "OPTIONS"  # Indicate that options menu should be shown

        screen.fill(BLACK)
        
        # Render the bigger title using the menu_title_font
        draw_text("Game Title", menu_title_font, (0, 255, 255), screen_width // 2, screen_height // 4)
        draw_text("Main Menu", font, (255, 255, 255), screen_width // 2, screen_height // 2.5)
        
        draw_text("Press (s) to Start Game", font, (255, 0, 0), screen_width // 2, screen_height // 2)
        draw_text("Press (o) for Options", font, (255, 255, 255), screen_width // 2, (screen_height // 2) + 50)
        draw_text("Press (q) to Quit", font, (255, 255, 255), screen_width // 2, (screen_height // 2) + 100)

        pygame.display.flip()

def options_menu():
    running = True

   
    sound_enabled = True  # Initialize sound option

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "MENU"  # Indicate that the main menu should be shown
               
                if event.key == pygame.K_s:
                    sound_enabled = not sound_enabled

        screen.fill(BLACK)
        draw_text("Options Menu", menu_title_font, (WHITE), screen_width // 2, screen_height // 4)
        draw_text("Press (s) Sound: " + ("On" if sound_enabled else "Off"), font, (255, 255, 255), screen_width // 2, (screen_height // 2) + 50)
        draw_text("Press (q) to go Back to Main Menu", font, (255, 0, 0), screen_width // 2, (screen_height // 2) + 100)

        pygame.display.flip()

if __name__ == "__main__":
    current_menu = main_menu()
    while True:
        if current_menu == "PLAY":
            print("Starting the game...")
            break
        elif current_menu == "OPTIONS":
            current_menu = options_menu()
        elif current_menu == "MENU":
            current_menu = main_menu()
