from scenes.battle_scene import BattleScene
from scenes.dialog_scene import DialogScene
from scenes.loot_scene import LootScene


class BattleTrigger:
    def __init__(self, monster):
        self.monster = monster

    def activate(self, game):
        game.scene_manager.change_scene(
            BattleScene(game, game.party, [self.monster])
        )

class DialogTrigger:
    def __init__(self, npc):
        self.npc = npc

    def activate(self, game):
        game.scene_manager.change_scene(
            DialogScene(game, self.npc)
        )

class LootTrigger:
    def __init__(self, chest):
        self.chest = chest

    def activate(self, game):
        game.scene_manager.change_scene(
            LootScene(game, game.party, self.chest)
        )