from utils.loader import AssetLoader
import pygame
import os
import random
from utils.constants import TILE_SIZE, ASSETS_DIR

class TileRegistry:
    FLOOR = pygame.Surface((32, 32))
    FLOOR_VARIANTS = []
    VOID = pygame.Surface((32, 32))
    EXIT = pygame.Surface((32, 32))


    @classmethod
    def init(cls):
        # Загрузка всех вариантов пола
        floors_dir = os.path.join(ASSETS_DIR, "tiles", "floors")
        if os.path.exists(floors_dir):
            for filename in os.listdir(floors_dir):
                if filename.endswith(".png"):
                    floor_img = AssetLoader.load_image(f"tiles/floors/{filename}", scale=(TILE_SIZE, TILE_SIZE))
                    cls.FLOOR_VARIANTS.append(floor_img)
        
        # Если нет вариантов, загружаем основной
        if not cls.FLOOR_VARIANTS:
            cls.FLOOR = AssetLoader.load_image("tiles/floor.png", scale=(TILE_SIZE, TILE_SIZE))
            cls.FLOOR_VARIANTS = [cls.FLOOR]
        else:
            cls.FLOOR = cls.FLOOR_VARIANTS[0]
        
        cls.FLOOR_DARK = cls._make_dark(cls.FLOOR)
        cls.VOID = AssetLoader.load_image("tiles/void.png", scale=(TILE_SIZE, TILE_SIZE))
        cls.EXIT = AssetLoader.load_image("tiles/exit_room.png", scale=(TILE_SIZE, TILE_SIZE))
    
    @classmethod
    def get_random_floor(cls):
        return random.choice(cls.FLOOR_VARIANTS)

    @staticmethod
    def _make_dark(surface, factor=0.45):
        dark = surface.copy()
        overlay = pygame.Surface(dark.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(255 * (1 - factor))))
        dark.blit(overlay, (0,0))
        return dark