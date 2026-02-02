from core.scene import Scene
from scenes.dungeon_scene import DungeonScene
from systems.combat_system import CombatSystem

class BattleScene(Scene):
    def __init__(self, game, party, enemies):
        super().__init__(game)
        self.combat = CombatSystem(party, enemies)

    def update(self, dt):
        if self.combat.is_finished():
            self.game.scene_manager.change_scene(
                DungeonScene(...)
            )