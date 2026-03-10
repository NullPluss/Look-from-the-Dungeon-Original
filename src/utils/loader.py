import os
import pygame
from utils.constants import ASSETS_DIR


class AssetLoader:
    _cache = {}

    @classmethod
    def load_image(cls, relative_path, scale=None, max_height=None):
        cache_key = f"{relative_path}_{scale}_{max_height}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]

        full_path = os.path.join(ASSETS_DIR, relative_path)

        try:
            image = pygame.image.load(full_path)

            if pygame.display.get_init():
                image = image.convert_alpha()

            if scale:
                image = pygame.transform.scale(image, scale)
            elif max_height:
                # Масштабирование с сохранением пропорций
                w, h = image.get_size()
                aspect_ratio = w / h
                new_h = max_height
                new_w = int(max_height * aspect_ratio)
                image = pygame.transform.smoothscale(image, (new_w, new_h))

        except Exception as e:
            print(f"[ASSET ERROR] {full_path}: {e}")
            image = pygame.Surface(scale or (32, 32))
            image.fill((255, 0, 255))

        cls._cache[cache_key] = image
        return image
