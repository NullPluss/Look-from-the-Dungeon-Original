from entities.entity import Entity

class NPC(Entity):
    def __init__(self, pos, npc_type):
        super().__init__(pos)
        self.npc_type = npc_type
        self.name = npc_type["name"]
        self.profession = npc_type["profession"]
        self.quest_item = npc_type["quest_item"]
        self.dialogue = npc_type["dialogue"]
        self.hp = npc_type["hp"]
        self.max_hp = npc_type["hp"]
        self.mp = npc_type["mp"]
        self.max_mp = npc_type["mp"]
        self.image = npc_type["image"]
        
        self.quest_completed = False
        self.in_party = False
        self.can_recruit = True

    def interact(self, player, game):
        game.event_manager.emit("START_DIALOG", npc=self)