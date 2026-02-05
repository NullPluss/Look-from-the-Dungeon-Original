from utils.loader import AssetLoader
import pygame
from utils.constants import TILE_SIZE

class TileRegistry:
    FLOOR = pygame.Surface((32, 32), masks=((15, 15, 15)))
    VOID = pygame.Surface((32, 32), masks=((50, 50, 50)))
    EXIT = pygame.Surface((32, 32), masks=((200, 50, 50)))


    @classmethod
    def init(cls):
        cls.FLOOR = AssetLoader.load_image("tiles/floor.png", scale=(TILE_SIZE, TILE_SIZE))
        cls.FLOOR_DARK = cls._make_dark(cls.FLOOR)
        cls.VOID  = AssetLoader.load_image("tiles/void.png", scale=(TILE_SIZE, TILE_SIZE))
        cls.EXIT = AssetLoader.load_image("tiles/exit_room.png", scale=(TILE_SIZE, TILE_SIZE))

    @staticmethod
    def _make_dark(surface, factor=0.45):
        dark = surface.copy()
        overlay = pygame.Surface(dark.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(255 * (1 - factor))))
        dark.blit(overlay, (0,0))
        return dark