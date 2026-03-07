from entities.entity import Entity
from utils.asset_registry import AssetRegistry

class Monster(Entity):
    def __init__(self, pos, monster_type):
        super().__init__(pos)
        self.monster_type = monster_type
        self.hp = monster_type["hp"]
        self.max_hp = monster_type["hp"]
        self.mp = monster_type["mp"]
        self.max_mp = monster_type["mp"]
        self.damage = monster_type["damage"]
        self.loot = monster_type["loot"]
        self.image = monster_type["image"]

    def interact(self, player, game):
        game.event_manager.emit("START_COMBAT", enemy=self)
