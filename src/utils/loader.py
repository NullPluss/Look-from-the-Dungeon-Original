import pygame
import os


class AssetLoader:
    _cache = {}

    @classmethod
    def load_image(cls, path, colorkey=None, scale=None):
        if path in cls._cache:
            return cls._cache[path]

        image = pygame.image.load(path).convert_alpha()

        if colorkey:
            image.set_colorkey(colorkey)

        if scale:
            image = pygame.transform.scale(image, scale)

        cls._cache[path] = image
        return image