from entities.entity import Entity
from utils.asset_registry import AssetRegistry

class Chest(Entity):
    def __init__(self, pos):
        super().__init__(pos)
        self.opened = False
        self.image = AssetRegistry.CHEST

    def interact(self, player, game):
        if self.opened:
            return

        self.opened = True
        game.event_manager.emit("OPEN_CHEST", chest=self)
