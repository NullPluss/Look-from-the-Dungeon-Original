from systems.combat_system import CombatSystem
from entities.chest import Chest


class Scene():
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass

class BattleScene(Scene):
    def __init__(self, game, party, enemies):
        super().__init__(game)
        self.combat = CombatSystem(party, enemies)

    def on_enter(self): pass
    def on_exit(self): pass
    def update(self, dt): pass
    def render(self, screen): pass
    def handle_event(self, event): pass


class DialogScene(Scene):
    def __init__(self, game, npc):
        super().__init__(game)
        self.npc = npc
    
    def on_enter(self): pass
    def on_exit(self): pass
    def update(self, dt): pass
    def render(self, screen): pass
    def handle_event(self, event): pass

class InventoryScene(Scene):
    def __init__(self, game, party):
        super().__init__(game)
        self.party = party

    def on_enter(self): pass
    def on_exit(self): pass
    def update(self, dt): pass
    def render(self, screen): pass
    def handle_event(self, event): pass


class LootScene(Scene):
    def __init__(self, game, party, chest: Chest):
        super().__init__(game)
        self.party = party
        self.chest = chest

    def on_enter(self): pass
    def on_exit(self): pass
    def update(self, dt): pass
    def render(self, screen): pass
    def handle_event(self, event): pass
