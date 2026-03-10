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
    
    NPC_ALCHEMIST = pygame.Surface((32, 32))
    NPC_BARD = pygame.Surface((32, 32))
    NPC_BLACKSMITH = pygame.Surface((32, 32))
    NPC_DEALER = pygame.Surface((32, 32))
    NPC_DOCTOR = pygame.Surface((32, 32))
    NPC_HUNTER = pygame.Surface((32, 32))
    NPC_JEWELER = pygame.Surface((32, 32))
    NPC_MAGE = pygame.Surface((32, 32))
    NPC_SAGE = pygame.Surface((32, 32))
    NPC_TRAVELER = pygame.Surface((32, 32))

    @classmethod
    def init(cls):
        cls.PLAYER = AssetLoader.load_image("entities/player.png", scale=(60, 110))
        cls.CHEST = AssetLoader.load_image("entities/chests/chest.png", scale=(60, 60))
        
        cls.GOBLIN_MAGE = AssetLoader.load_image("entities/monsters/goblin_mage.png", scale=(90, 90))
        cls.GOBLIN_WARRIOR = AssetLoader.load_image("entities/monsters/goblin_warior.png", scale=(90, 90))
        cls.SKELETON = AssetLoader.load_image("entities/monsters/skelet.png", scale=(90, 90))
        cls.SKELETON_WARRIOR = AssetLoader.load_image("entities/monsters/skelet_warior.png", scale=(90, 90))
        cls.SKELETON_HUNTMAN = AssetLoader.load_image("entities/monsters/skelet_huntman.png", scale=(90, 90))
        
        cls.NPC_ALCHEMIST = AssetLoader.load_image("entities/npc/alchemist.png", max_height=110)
        cls.NPC_BARD = AssetLoader.load_image("entities/npc/bard.png", max_height=110)
        cls.NPC_BLACKSMITH = AssetLoader.load_image("entities/npc/blacksmith.png", max_height=110)
        cls.NPC_DEALER = AssetLoader.load_image("entities/npc/dealer.png", max_height=110)
        cls.NPC_DOCTOR = AssetLoader.load_image("entities/npc/doctor.png", max_height=110)
        cls.NPC_HUNTER = AssetLoader.load_image("entities/npc/hunter.png", max_height=110)
        cls.NPC_JEWELER = AssetLoader.load_image("entities/npc/jeweler.png", max_height=110)
        cls.NPC_MAGE = AssetLoader.load_image("entities/npc/mage.png", max_height=110)
        cls.NPC_SAGE = AssetLoader.load_image("entities/npc/sage.png", max_height=110)
        cls.NPC_TRAVELER = AssetLoader.load_image("entities/npc/traveler.png", max_height=110)