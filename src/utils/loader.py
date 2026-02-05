import os
import pygame
from utils.constants import ASSETS_DIR


class AssetLoader:
    _cache = {}

    @classmethod
    def load_image(cls, relative_path, scale=None):
        if relative_path in cls._cache:
            return cls._cache[relative_path]

        full_path = os.path.join(ASSETS_DIR, relative_path)

        try:
            image = pygame.image.load(full_path)

            if pygame.display.get_init():
                image = image.convert_alpha()

            if scale:
                image = pygame.transform.scale(image, scale)

        except Exception as e:
            print(f"[ASSET ERROR] {full_path}: {e}")
            image = pygame.Surface(scale or (32, 32))
            image.fill((255, 0, 255))

        cls._cache[relative_path] = image
        return image
