from utils.asset_registry import AssetRegistry

def get_monster_types():
    return {
        "goblin_mage": {
            "hp": 50,
            "mp": 50,
            "damage": 30,
            "loot": "fireball_scroll",
            "image": AssetRegistry.GOBLIN_MAGE
        },
        "goblin_warrior": {
            "hp": 75,
            "mp": 0,
            "damage": 40,
            "loot": "sword",
            "image": AssetRegistry.GOBLIN_WARRIOR
        },
        "skeleton_huntman": {
            "hp": 50,
            "mp": 0,
            "damage": 35,
            "loot": "bow_and_arrows",
            "image": AssetRegistry.SKELETON_HUNTMAN
        },
        "skeleton": {
            "hp": 25,
            "mp": 25,
            "damage": 20,
            "loot": "bone",
            "image": AssetRegistry.SKELETON
        }
    }
