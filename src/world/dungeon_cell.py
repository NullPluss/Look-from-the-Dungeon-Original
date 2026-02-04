import pygame
from utils.layout import LayoutCell
from world.tile_registry import TileRegistry

class DungeonCell:

    TILE_SIZE = 360

    def __init__(self, x, y, size, tile_type):
        self.rect = pygame.Rect(x, y, size, size)
        self.tile_type = tile_type

        # self.image = pygame.Surface((size, size))

        # if tile_type == LayoutCell.VOID:
        #     self.image.fill((50, 50, 50))
        # elif tile_type == LayoutCell.FLOOR:
        #     self.image.fill((15, 15, 15))
        # elif tile_type == LayoutCell.EXIT:
        #     self.image.fill((200, 50, 50))
        # elif tile_type == LayoutCell.START:
        #     self.image.fill((50, 200, 50))

        self.image = self._load_texture(tile_type)

    def _load_texture(self, tile_type):
        if tile_type == LayoutCell.FLOOR:
            return TileRegistry.FLOOR
        
        if tile_type == LayoutCell.VOID:
            return TileRegistry.VOID
            

        surf = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
        surf.fill((0, 0, 0))
        return surf