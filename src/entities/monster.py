from entities.entity import Entity
class Monster(Entity):
    def __init__(self, pos, stats):
        super().__init__(pos)
        self.stats = stats

    def interact(self, player, game):
        game.event_manager.emit("START_COMBAT", enemy=self)
