from entities.entity import Entity
from utils.asset_registry import AssetRegistry

class Monster(Entity):
    def __init__(self, pos, monster_type):
        super().__init__(pos)
        self.monster_type = monster_type
        self.name = monster_type["name"]
        self.hp = monster_type["hp"]
        self.max_hp = monster_type["hp"]
        self.mp = monster_type["mp"]
        self.max_mp = monster_type["mp"]
        self.damage = monster_type["damage"]
        self.attack_type = monster_type["attack_type"]
        self.attack_range = monster_type["attack_range"]
        self.mp_cost = monster_type.get("mp_cost", 0)
        self.loot = monster_type["loot"]
        self.image = monster_type["image"]

    def interact(self, player, game):
        game.event_manager.emit("START_COMBAT", enemy=self)
