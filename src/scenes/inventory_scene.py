import pygame
from core.scene import Scene
from systems.events import OpenInventoryEvent

class InventoryScene(Scene):
    def __init__(self, game, party):
        super().__init__(game)
        self.party = party

    def handle_event(self, event):
        if event.key == pygame.K_i:
            self.game.scene_manager.change_scene(
                self.game.last_scene
            )
        
        if event.key == pygame.K_i:
            self.game.event_manager.emit(OpenInventoryEvent())