import pygame
from settings import *
from tile import Tile
from playerr import Player
from debug import debug


class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.barrier_sprites = pygame.sprite.Group()

        self.player = None
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                # tilesize = 64
                x, y = col_index * tilesize, row_index * tilesize
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.barrier_sprites])
                if col == 'p':
                    self.player = Player((x, y),
                                         [self.visible_sprites], self.barrier_sprites)

    def run(self):
        self.visible_sprites.draw(self.screen)
        self.visible_sprites.update()
        debug(self.player.direction)
