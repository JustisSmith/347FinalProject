import pygame
import actor

from settings import *
from level1 import Level1

class Game:
    def __init__(self):
        """
        Start up Pygame and instantiate all
        relevant actors.
        @width : sets width of the screen
        @height : sets height of the screen
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.level = Level1(level1_map, self.screen)


        # this allows us to filter the event queue
        # for faster event processing
        pygame.event.set_allowed([
            pygame.QUIT,
            pygame.KEYDOWN
        ])

        self.player = actor.Player(0, 0)

        # colliders put right off-screen on both sides in order
        # to keep player from walking off the edge
        collider_left = actor.Collider(pygame.Rect(-1, 0, 1, screen_height))
        collider_right = actor.Collider(pygame.Rect(screen_width+1, 0, 1, screen_height))

        """
        self.collider_ground = actor.Collider(
            pygame.Rect(0, screen_height-40, screen_width, 40), color="chartreuse4"
        )
        """
        
        # sprite groups allows us to perform batch
        # collision detection, as seen in Player.update()
        self.colliders = pygame.sprite.Group(
            collider_left, collider_right, 
            #self.collider_ground,
            *self.level.get_tiles()
        )

    def loop(self):
        """
        Primary game loop. This should be
        run perpetually until the game is
        over or is closed.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                
            self.screen.fill("black")
            self.level.run()
                
            self.player.processInput(pygame.key.get_pressed())
            self.player.update(self.colliders)
            self.player.render(self.screen)
            #self.collider_ground.render(self.screen)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.player = actor.Player(100, 500, game)
    game.loop()