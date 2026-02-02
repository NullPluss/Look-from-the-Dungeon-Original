class GameEvent:
    pass

class StartBattleEvent(GameEvent):
    def __init__(self, enemies):
        self.enemies = enemies

class EndBattleEvent(GameEvent):
    def __init__(self, victory):
        self.victory = victory

class OpenInventoryEvent(GameEvent):
    def __init__(self, inventory):
        self.inventory = inventory

class OpenMapEvent(GameEvent):
    def __init__(self, map_data):
        self.map_data = map_data   

class NPCDialogEvent(GameEvent):
    def __init__(self, npc):
        self.npc = npc

class QuestCompletedEvent(GameEvent):
    def __init__(self, quest):
        self.quest = quest

class StartDialogEvent(GameEvent):
    def __init__(self, npcs):
        self.npcs = npcs

class StartOpenChestEvent(GameEvent):
    def __init__(self, chests):
        self.chests = chests