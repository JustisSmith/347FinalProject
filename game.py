import pygame
import actor
from settings import *
from level1 import Level1
from enum import Enum
from menu import main_menu, options_menu  

class GameState(Enum):
    MENU = 0
    OPTIONS = 1
    PLAY = 2

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.level = Level1(level1_map, self.screen)

        pygame.event.set_allowed([
            pygame.QUIT,
            pygame.KEYDOWN
        ])

        self.player = actor.Player(0, 0)

        collider_left = actor.Collider(pygame.Rect(-1, 0, 1, screen_height))
        collider_right = actor.Collider(pygame.Rect(screen_width + 1, 0, 1, screen_height))

        self.colliders = pygame.sprite.Group(
            collider_left, collider_right,
            *self.level.get_tiles()
        )

        self.game_state = GameState.MENU

        # New attribute for the timer
        self.timer = 0
        self.timer_font = pygame.font.Font(None, 36)

    def set_game_state(self, new_state):
        self.game_state = new_state
    
    #incrementes the timer 
    def update_timer(self, dt):
        if self.game_state == GameState.PLAY:
            self.timer += dt

    # method that depicts the timer in the top right corner 
    def draw_timer(self):
        if self.game_state == GameState.PLAY:
            timer_text = self.timer_font.render(f"Time: {int(self.timer)} seconds", True, (255, 255, 255))
            timer_rect = timer_text.get_rect()
            timer_rect.topleft = (screen_width - timer_rect.width - 10, 10)
            self.screen.blit(timer_text, timer_rect.topleft)

    def loop(self):
        while True:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if self.game_state == GameState.PLAY and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.set_game_state(GameState.MENU)

            if self.game_state == GameState.MENU:
                current_menu = main_menu()
                if current_menu == "PLAY":
                    self.set_game_state(GameState.PLAY)
                elif current_menu == "OPTIONS":
                    self.set_game_state(GameState.OPTIONS)
                elif current_menu == "QUIT":
                    pygame.quit()
                    return
            elif self.game_state == GameState.OPTIONS:
                current_menu = options_menu()
                if current_menu == "MENU":
                    self.set_game_state(GameState.MENU)
            elif self.game_state == GameState.PLAY:
                self.screen.fill("black")
                self.level.run()

                self.player.processInput(pygame.key.get_pressed())
                self.player.update(self.colliders)
                self.player.render(self.screen)

                self.update_timer(dt)
                self.draw_timer()

                pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.player = actor.Player(0, 0, game)
    game.loop()
      
       
          
