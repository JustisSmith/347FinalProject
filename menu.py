import pygame
import sys
from settings import screen_width, screen_height

pygame.init()

# Create a window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu")

# Load background image
background_image = pygame.image.load("menu_background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Scale the image to fit the screen

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
menu_title_font = pygame.font.Font(None, 72)
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
                    return "PLAY"
                if event.key == pygame.K_o:
                    return "OPTIONS"

        # Blit the background image
        screen.blit(background_image, (0, 0))

        draw_text("Game Title", menu_title_font, (0, 255, 255), screen_width // 2, screen_height // 4)
        draw_text("Main Menu", font, (255, 255, 255), screen_width // 2, screen_height // 2.5)
        
        draw_text("Press (s) to Start Game", font, (255, 0, 0), screen_width // 2, screen_height // 2)
        draw_text("Press (o) for Options", font, (255, 255, 255), screen_width // 2, (screen_height // 2) + 50)
        draw_text("Press (q) to Quit", font, (255, 255, 255), screen_width // 2, (screen_height // 2) + 100)

        pygame.display.flip()

def options_menu():
    running = True
    sound_enabled = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "MENU"
                if event.key == pygame.K_s:
                    sound_enabled = not sound_enabled

        # Blit the background image
        screen.blit(background_image, (0, 0))

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
