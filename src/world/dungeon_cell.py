import pygame
from utils.layout import LayoutCell
from world.tile_registry import TileRegistry
from utils.constants import TILE_SIZE


class DungeonCell:
    def __init__(self, x, y, size, tile_type):
        self.rect = pygame.Rect(x, y, size, size)
        self.tile_type = tile_type
        self.explored = False
        self.visible = False
        self.x = x // TILE_SIZE
        self.y = y // TILE_SIZE
        
        self.image = self._load_texture(tile_type)


    def _load_texture(self, tile_type):
        if tile_type == LayoutCell.FLOOR:
            return TileRegistry.FLOOR
        
        if tile_type == LayoutCell.VOID:
            return TileRegistry.VOID
        
        if tile_type == LayoutCell.EXIT:
            return TileRegistry.EXIT
        
        if tile_type == LayoutCell.START:
            return TileRegistry.FLOOR