from utils.loader import AssetLoader
import pygame

class AssetRegistry:
    PLAYER = pygame.Surface((32, 32))
    CHEST = pygame.Surface((32, 32))

    @classmethod
    def init(cls):
        cls.PLAYER = AssetLoader.load_image("entities/player.png", scale=(60, 110))
        cls.CHEST = AssetLoader.load_image("entities/chests/chest.png", scale=(60, 60))