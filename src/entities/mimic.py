from entities.chest import Chest

class Mimic(Chest):
    def interact(self, player, game):
        game.event_manager.emit("START_COMBAT", enemy=self)
