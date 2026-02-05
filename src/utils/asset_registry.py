from utils.loader import AssetLoader
import pygame

class AssetRegistry:
    PLAYER = pygame.Surface((32, 32), masks=((15, 15, 15)))

    @classmethod
    def init(cls):
        cls.PLAYER = AssetLoader.load_image("entities/player.png", scale=(60, 110))