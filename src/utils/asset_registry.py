from utils.loader import AssetLoader
import pygame

class AssetRegistry:
    PLAYER = pygame.Surface((32, 32))
    CHEST = pygame.Surface((32, 32))
    
    GOBLIN_MAGE = pygame.Surface((32, 32))
    GOBLIN_WARRIOR = pygame.Surface((32, 32))
    SKELETON = pygame.Surface((32, 32))
    SKELETON_WARRIOR = pygame.Surface((32, 32))
    SKELETON_HUNTMAN = pygame.Surface((32, 32))

    @classmethod
    def init(cls):
        cls.PLAYER = AssetLoader.load_image("entities/player.png", scale=(60, 110))
        cls.CHEST = AssetLoader.load_image("entities/chests/chest.png", scale=(60, 60))
        
        cls.GOBLIN_MAGE = AssetLoader.load_image("entities/monsters/goblin_mage.png", scale=(90, 90))
        cls.GOBLIN_WARRIOR = AssetLoader.load_image("entities/monsters/goblin_warior.png", scale=(90, 90))
        cls.SKELETON = AssetLoader.load_image("entities/monsters/skelet.png", scale=(90, 90))
        cls.SKELETON_WARRIOR = AssetLoader.load_image("entities/monsters/skelet_warior.png", scale=(90, 90))
        cls.SKELETON_HUNTMAN = AssetLoader.load_image("entities/monsters/skelet_huntman.png", scale=(90, 90))