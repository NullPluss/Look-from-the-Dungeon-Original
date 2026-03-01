from entities.entity import Entity

class NPC(Entity):
    def __init__(self, pos, dialogue):
        super().__init__(pos)
        self.dialogue = dialogue

    def interact(self, player, game):
        game.event_manager.emit("START_DIALOG", npc=self)

    def update(self, dt):
        pass