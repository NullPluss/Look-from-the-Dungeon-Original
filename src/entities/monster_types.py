from utils.asset_registry import AssetRegistry

def get_monster_types():
    return {
        "goblin_warrior": {
            "name": "Гоблин-воин",
            "hp": 100,
            "mp": 0,
            "damage": 40,
            "attack_type": "melee",
            "attack_range": 1,
            "loot": ["Меч", "Зелье здоровья"],
            "image": AssetRegistry.GOBLIN_WARRIOR,
            "weight": 50
        },
        "skeleton_warrior": {
            "name": "Скелет-воин",
            "hp": 100,
            "mp": 0,
            "damage": 40,
            "attack_type": "melee",
            "attack_range": 1,
            "loot": ["Меч", "Зелье здоровья"],
            "image": AssetRegistry.SKELETON_WARRIOR,
            "weight": 50
        },
        "goblin_mage": {
            "name": "Гоблин-маг",
            "hp": 40,
            "mp": 50,
            "damage": 100,
            "attack_type": "ranged",
            "attack_range": 2,
            "mp_cost": 50,
            "loot": ["Свиток огненного шара", "Зелье маны"],
            "image": AssetRegistry.GOBLIN_MAGE,
            "weight": 20
        },
        "skeleton_huntman": {
            "name": "Скелет-охотник",
            "hp": 50,
            "mp": 0,
            "damage": 50,
            "attack_type": "ranged",
            "attack_range": 4,
            "loot": ["Арбалет", "Шкура дикого зверя", "Арбалетные болты"],
            "loot_counts": {"Арбалетные болты": 10},
            "image": AssetRegistry.SKELETON_HUNTMAN,
            "weight": 30
        }
    }
