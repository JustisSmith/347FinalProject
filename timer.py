import pygame

class Timer:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.start_time = pygame.time.get_ticks()

    def get_elapsed_time(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) // 1000  # Convert milliseconds to seconds
        return elapsed_time

    def render(self, screen):
        elapsed_time = self.get_elapsed_time()

        # Render black background for high contrast 
        background_rect = pygame.Rect(screen.get_width() - 210, 10, 200, 40)
        pygame.draw.rect(screen, (0, 0, 0), background_rect)

        # Render the timer text on top of the black background
        timer_text = self.font.render(f"Time: {elapsed_time}s", True, (255, 255, 255))
        text_rect = timer_text.get_rect(center=background_rect.center)
        screen.blit(timer_text, text_rect.topleft)

