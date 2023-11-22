import pygame
from tiles import Tile
from settings import tile_size

class Level1:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.level_data = level_data
        self.setup_level(level_data)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        for row_index,row in enumerate(layout):
            for col_index,cell in enumerate(row):
                if cell == 'X':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    #tile == Tile((x, y), tile_size)
                    self.tiles.add(Tile((x,y), tile_size))

    def get_tiles(self):
        return self.tiles

    """
    def horizontal_movement_collision(self):
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect)
    """       

    def run(self):
        self.tiles.draw(self.display_surface)
