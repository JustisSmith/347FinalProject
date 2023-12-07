# Imports the necessary libraries
import pygame
import sys
from settings import screen_width, screen_height

# Initialize the Pygame library
pygame.init()

# Create a window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu")

# Load background image
background_image = pygame.image.load("menu_background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Scales the image to fit the screen

# Defined color constants 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define fonts
menu_title_font = pygame.font.Font(None, 72)
font = pygame.font.Font(None, 36)

# variable for sound state
sound_enabled = True

# Function to draw text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Function for the main menu
def main_menu():
    running = True
    global sound_enabled

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

        # Display main menu text
        draw_text("Game Title", menu_title_font, (0, 255, 255), screen_width // 2, screen_height // 4)
        draw_text("Main Menu", font, (255, 255, 255), screen_width // 2, screen_height // 2.5)
        
        draw_text("Press (s) to Start Game", font, (255, 0, 0), screen_width // 2, screen_height // 2)
        draw_text("Press (o) for Options", font, (255, 255, 255), screen_width // 2, (screen_height // 2) + 50)
        draw_text("Press (q) to Quit", font, (255, 255, 255), screen_width // 2, (screen_height // 2) + 100)

        pygame.display.flip()

# Function for the options menu
def options_menu():
    running = True
    global sound_enabled

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
                if event.key == pygame.K_c:
                    controls_menu()

        # Blit the background image
        screen.blit(background_image, (0, 0))

        # Displays the options menu text
        draw_text("Options Menu", menu_title_font, (WHITE), screen_width // 2, screen_height // 4)
        draw_text("Press (s) Sound: " + ("On" if sound_enabled else "Off"), font, (255, 255, 255), screen_width // 2, (screen_height // 3) + 50)
        draw_text("Press (c) for Controls", font, (255, 255, 255), screen_width // 2, (screen_height // 3) + 100)
        draw_text("Press (q) to go Back to Main Menu", font, (255, 0, 0), screen_width // 2, (screen_height // 2) + 150)

        pygame.display.flip()

# New function for the controls menu
def controls_menu():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return

        # Blit the background image
        screen.blit(background_image, (0, 0))

        # Displays the controls menu text
        draw_text("Controls ", menu_title_font, (WHITE), screen_width // 2, screen_height // 4)
        # Add additional controls information here
        draw_text("Movement: use the ARROW keys to move from left to right  ", font, (255,255, 0), screen_width // 2, (screen_height // 3) + 25)
        draw_text("Jump: use the SPACE key to jump  ", font, (255,255,0), screen_width // 2, (screen_height // 3) + 75)
        draw_text("Wall slide: approach a wall and jump to begin sliding ", font, (255,255,0), screen_width // 2, (screen_height // 3) + 125)

        draw_text("Press (q) to go Back to Options Menu", font, (255, 0, 0), screen_width // 2, (screen_height // 2) + 150)

        

        pygame.display.flip()

if __name__ == "__main__":
    # Starts with the main menu
    current_menu = main_menu()
    
    # Loop to navigate between menus
    while True:
        if current_menu == "PLAY":
            print("Starting the game...")
            break
        elif current_menu == "OPTIONS":
            current_menu = options_menu()
        elif current_menu == "MENU":
            current_menu = main_menu()

